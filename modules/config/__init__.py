"""Config Module

Handling all the config (.yml/.env) files

TODO:
    - Fully remove config.yml and migrate to database
"""
from dotenv import load_dotenv

load_dotenv('storage/data/.env', override=True, verbose=True)

from .yml import *
from .functions import *
from .values import *


