"""Config Module

Handling all the config (.yml/.env) files"""

from dotenv import load_dotenv

load_dotenv('storage/data/.env', override=True, verbose=True)

from .yml import *

from .env_values import *
from .config_values import *


