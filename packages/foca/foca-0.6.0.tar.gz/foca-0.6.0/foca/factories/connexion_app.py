"""Factory for creating and configuring Connexion app instances."""

from inspect import stack
import logging
from typing import Optional

from connexion import App

from foca.models.config import Config

# Get logger instance
logger = logging.getLogger(__name__)


def create_connexion_app(config: Optional[Config] = None) -> App:
    """Create and configure Connexion app."""
    # Instantiate Connexion app
    app = App(
        __name__,
        skip_error_handlers=True,
    )

    calling_module = ':'.join([stack()[1].filename, stack()[1].function])
    logger.debug(f"Connexion app created from '{calling_module}'.")

    # Configure Connexion app
    if config is not None:
        app = __add_config_to_connexion_app(
            app=app,
            config=config,
        )

    return app


def __add_config_to_connexion_app(
    app: App,
    config: Config,
) -> App:
    """Replace default Connexion and Flask app settings and add FOCA- and user-
    defined configuration parameters to Flask app.

    Args:
        app: Connexion app.
        config: App configuration.

    Returns:
        Connexion app.
    """
    conf = config.server

    # replace Connexion app settings
    app.host = conf.host
    app.port = conf.port
    app.debug = conf.debug

    # replace Flask app settings
    app.app.config['DEBUG'] = conf.debug
    app.app.config['ENV'] = conf.environment
    app.app.config['TESTING'] = conf.testing

    logger.debug('Flask app settings:')
    for (key, value) in app.app.config.items():
        logger.debug('* {}: {}'.format(key, value))

    # Add user configuration to Flask app config
    app.app.config['FOCA'] = config

    logger.debug('Connexion app configured.')
    return app
