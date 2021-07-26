"""Utils Module

Methods that are used widely over the project
"""
from .functions import *
from .logging import *
from .validations import *

from modules.config import Env

add_main_logger_handler()
add_debug_logger_handler()

if Env.LOG_DEBUG_DISCORD:
    logger = add_discord_logger_handler()
    logger.info('Discord Debug logger handler added')
