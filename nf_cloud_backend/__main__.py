from logging.config import dictConfig

# internal imports
from nf_cloud_backend.command_line_interface import ComandLineInterface


def main():
    """
    Main function
    """
    cli = ComandLineInterface()
    cli.start()


if __name__ == "__main__":
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(filename)s:%(lineno)s - %(funcName)20s()] %(levelname)s in %(module)s:\n\t %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "DEBUG", "handlers": ["wsgi"]},
        }
    )
    main()
