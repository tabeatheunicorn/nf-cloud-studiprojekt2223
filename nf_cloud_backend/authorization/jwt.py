# std imports
import datetime
import logging
from typing import ClassVar, Tuple

# internal imports
from nf_cloud_backend.models.user import User

# 3rd party imports
import jwt

logger = logging.getLogger(__file__)
class JWT:
    """
    Class to encode and decode JWT tokens. Algorithm is hardcoded as ClassVar
    Is a wrapper to given jwt module
    """

    # TODO Offer more sigingn algorithms as type?
    SIGNING_ALGORTIHTM: ClassVar[str] = "HS256"

    # TODO Secret should probably be loaded from ENV
    @classmethod
    def create_auth_token(cls, secret_key: str, user: User, expires_at: int) -> str:
        """
        Creates an authentication token for the given user and provider. Internally uses jwt

        Parameters
        ----------
        secret_key : str
            Secret key for encoding
        user : User
            User

        Returns
        -------
        str
            JWT token
        """
        return jwt.encode(
            {
                "user_id": user.id,
                "expires_at": expires_at
            },
            secret_key,
            algorithm=cls.SIGNING_ALGORTIHTM
        )

    @classmethod
    def decode_auth_token(cls, secret_key: str, auth_token: str) -> dict:
        """
        Decoded the given JWT token from the given authentication header.

        Parameters
        ----------
        secret_key : str
            Secret key for encoding
        auth_header : str
            Header of format `JWT <jwt_token>`

        Returns
        -------
        dict
            Decoded payload
        """
        # TODO Expiration date should probably be checked?
        return jwt.decode(
            auth_token,
            secret_key,
            algorithms=[cls.SIGNING_ALGORTIHTM]
        )

    @classmethod
    def is_token_valid(cls, token_payload: dict) -> bool:
        """
        Checks if the token is still valid.

        Parameters
        ----------
        token_payload : dict
            Decoded token payload

        Returns
        -------
        bool
            True if valid.
        """
        raise NotImplementedError
        

    @classmethod
    def decode_auth_token_to_user(cls, secret_key: str, auth_token: str) -> Tuple[User, bool]:
        """
        Decoded the given JWT token from the given authentication header. 

        Parameters
        ----------
        secret_key : str
            Secret key for encoding
        auth_header : str
            Header of format `JWT <jwt_token>`

        Returns
        -------
        Tuple
            With user and if token was unexpired
        """
        data = cls.decode_auth_token(
            secret_key,
            auth_token
        )
        return User.select().where(
            User.id == data["user_id"]
        ).get_or_none(), data["expires_at"] > int(datetime.datetime.utcnow().timestamp())
