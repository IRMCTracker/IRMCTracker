from .functions import *
from .logging import *
from .validations import *

from modules.config import Env

add_main_logger_handler()
add_debug_logger_handler()

if Env.LOG_DEBUG_DISCORD:
    add_discord_logger_handler()
