"""
All configurations
"""
import logging
from typing import List

from pytconf import Config, ParamCreator, register_function

from pygooglehelper.auth import get_credentials
from pygooglehelper.static import LOGGER_NAME


class ConfigAuth(Config):
    force = ParamCreator.create_bool(
        help_string="Should we force creation of a new auth token",
        default=False,
    )
    # parameters passed to run_local_server
    host = ParamCreator.create_str(
        help_string="The hostname for the local redirect server. This will be served over http, not https",
        default='localhost',
    )
    port = ParamCreator.create_int(
        help_string="The port for the local redirect server",
        # default=8080,
        default=0,
    )
    # noinspection PyProtectedMember
    authorization_prompt_message = ParamCreator.create_str(
        help_string="The message to display to tell the user to navigate to the authorization URL",
        # default=InstalledAppFlow._DEFAULT_AUTH_PROMPT_MESSAGE,
        default="",
    )


def register_functions(scopes: List[str], app_name: str):
    register_function(
        function=close_auth(scopes, app_name),
        description="Do the authentication procedure and get token for your app",
        name="auth",
        configs=[ConfigAuth],
    )


def close_auth(scopes: List[str], app_name: str):
    def auth() -> None:
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        get_credentials(
            logger=logger,
            scopes=scopes,
            app_name=app_name,
            host=ConfigAuth.host,
            port=ConfigAuth.port,
            authorization_prompt_message=ConfigAuth.authorization_prompt_message,
            force=ConfigAuth.force,
        )
    return auth
