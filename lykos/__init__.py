from importlib.metadata import version

from loguru import logger as _logger

from .client import Client  # noqa: F401
from .errors import *  # noqa: F403

__version__ = version(__package__)

_logger.disable('lykos')
