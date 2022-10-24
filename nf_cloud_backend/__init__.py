# std importd
import json
import logging
import traceback
from threading import Thread
from typing import Optional, Tuple

# 3rd party imports
import eventlet
import jwt
from flask import Flask, Request
from flask import g as request_store
from flask import request
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from oauthlib.oauth2 import WebApplicationClient
from playhouse.flask_utils import FlaskDB
from werkzeug.exceptions import HTTPException

from nf_cloud_backend import \
    models  # Import module only to prevent circular imports
# internal imports
from nf_cloud_backend.constants import (ACCESS_TOKEN_HEADER,
                                        ONE_TIME_USE_ACCESS_TOKEN_CACHE_PREFIX,
                                        ONE_TIME_USE_ACCESS_TOKEN_PARAM_NAME)
from nf_cloud_backend.utility.configuration import Configuration, Environment
from nf_cloud_backend.utility.headers.cross_origin_resource_sharing import \
    add_allow_cors_headers
from nf_cloud_backend.utility.matomo import \
    track_request as matomo_track_request

# Load config and environment.
config, env = Configuration.get_config_and_env()

logger = logging.getLogger("FlaskApp")


def create_flask_app():
    """Create and configure Flask application.
    Allows CORS.
    Also sets config parameters.

    :return: configured Flask application instance
    """
    app = Flask("app")

    CORS(app)

    app.config.update(
        ENV=env.name,
        DEBUG=config["debug"],
        SECRET_KEY=config["secret"],
        PREFERRED_URL_SCHEME="https" if config["use_https"] else "http",
    )

    return app


def create_cache_for_flaskapp(app):
    """Cache for one time use authentication tokens"""
    cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 60})

    cache.init_app(app)
    return cache


def configure_socketio(app):
    """SocketIO for bidirectional communication (events) between server and browser."""
    async_mode = "threading"
    """Mode for SocketIO
    """
    if env == Environment.production:
        eventlet.monkey_patch()
        async_mode = "eventlet"
    # SocketIO for bi-directional
    socketio = SocketIO(app, cors_allowed_origins="*")

    socketio = SocketIO(
        app,
        message_queue=config["rabbit_mq"]["url"],
        cors_allowed_origins="*",
        async_mode=async_mode,
        engineio_logger=app.logger if config["debug"] else False,
        logger=config["debug"],
        always_connect=True,
    )
    return socketio


### setup and configure app, cache, db wrapper etc
app = create_flask_app()

cache = create_cache_for_flaskapp(app=app)
socketio = configure_socketio(app=app)

db_wrapper = FlaskDB(app, config["database"]["url"])
openid_clients = {
    provider: WebApplicationClient(provider_data["client_id"])
    for provider, provider_data in config["login_providers"]["openid"].items()
}

login_manager = LoginManager()
login_manager.init_app(app)

# Do not move import up, it would result in cyclic dependencies
from nf_cloud_backend.authorization.jwt import \
    JWT  # pylint: disable=wrong-import-position


@login_manager.request_loader
def load_user_from_request(incomming_request: Request):
    """
    Get user by Authorization-header.

    Parameters
    ----------
    incomming_request : Request
        Incomming request

    Returns
    -------
    User : optional
    """

    # Check if access token is provided in header
    auth_header = incomming_request.headers.get(ACCESS_TOKEN_HEADER, None)
    # If the JWT token isn't found in the header, try to resolve the JWT token by an one time use token
    # These are usually used for download URLs via the frontend where it is not possible to
    # add the access token to the headers and the file is too large fo the usual "Download -> Blob -> Blob download"-Javascript stuff.
    if auth_header is None:
        one_time_use_token: Optional[str] = incomming_request.args.get(
            ONE_TIME_USE_ACCESS_TOKEN_PARAM_NAME, None
        )
        one_time_use_token = (
            f"{ONE_TIME_USE_ACCESS_TOKEN_CACHE_PREFIX}{one_time_use_token}"
        )
        if cache.has(one_time_use_token):
            auth_header = cache.get(one_time_use_token)
            # Delete the one time use token from cache
            cache.delete(one_time_use_token)
        else:
            auth_header = None
    if auth_header is not None:
        try:
            user, is_unexpired = JWT.decode_auth_token_to_user(
                app.config["SECRET_KEY"], auth_header
            )
            if user is not None and is_unexpired:
                return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
    auth_header = incomming_request.headers.get("Authorization", None)
    if auth_header is not None:
        basic_auth = incomming_request.authorization
        if (
            basic_auth.username == config["worker_credentials"]["username"]
            and basic_auth.password == config["worker_credentials"]["password"]
        ):
            return models.user.User(
                id=0, provider_type="local", provider="local", login_id="worker"
            )
    return None


@app.before_request
def track_request():
    """
    Sends a tracking request to Matomo.
    """
    if config["matomo"]["enabled"]:
        track_thread = Thread(
            target=matomo_track_request,
            args=(
                request.headers.get("User-Agent", ""),
                request.remote_addr,
                request.headers.get("Referer", ""),
                request.headers.get("Accept-Language", ""),
                request.headers.get("Host", ""),
                request.full_path,
                request.query_string,
                request.url.startswith("https"),
                config["matomo"]["url"],
                config["matomo"]["site_id"],
                config["matomo"]["auth_token"],
                app,
                config["debug"],
            ),
        )
        track_thread.start()
        request_store.track_thread = track_thread


@app.teardown_appcontext
def wait_for_track_request(exception=None):  # pylint: disable=unused-argument
    """
    Waits for the Matomo tracking to finish.s

    Parameters
    ----------
    exception : Any, optional
        Required for `
    """
    track_thread = request_store.pop("track_thread", None)
    if track_thread:
        track_thread.join()


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Catching exceptions and sends them as requests.

    Parameters
    ----------
    e : Any
        Necessary for errorhandler

    Returns
    -------
    Response
        Response with formatted exception
    """
    response = None
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        # Return JSON instead of HTML for HTTP errors
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({"errors": {"general": e.description}})
        response.content_type = "application/json"
    else:
        response = app.response_class(
            response=json.dumps({"errors": {"general": str(e)}}),
            status=500,
            mimetype="application/json",
        )
    if config["debug"]:
        app.logger.error(traceback.format_exc())  # pylint: disable=no-member
        response = add_allow_cors_headers(response)
    return response


# Do not move this the top of the file, cause the modeule imports some values which are set during the initialization.
from nf_cloud_backend.utility.rabbit_mq import \
    RabbitMQ  # pylint: disable=wrong-import-position

RabbitMQ.prepare_queues()

# Import controllers.
# Do not move this import to the top of the files. Each controller uses 'app' to build the routes.
# Some controllers also import the connection pools.
from .controllers import *  # pylint: disable=wrong-import-position
