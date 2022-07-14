"""Utils Module

Methods that are used widely over the project
"""
from .functions import *
from .logging import *
from .validations import *
from .username_to_uuid import *
from .domain_tools import *

from modules.config import Config

add_main_logger_handler()
add_debug_logger_handler()

if Config.Log.DISCORD_DEBUG:
    logger = add_discord_logger_handler()
    logger.info('Discord Debug logger handler added')
