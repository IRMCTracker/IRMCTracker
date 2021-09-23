"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from datetime import datetime

from modules.utils.functions import shortified
from modules.database.models.vote import get_top_voted_servers
from modules.database import get_servers
from peewee import DoesNotExist

from modules.database.models.records import get_server_records

from urllib.request import urlopen
import json

import matplotlib.pyplot as plt

from modules.database import *

import uuid
from os import sep

from modules.utils import to_persian

create_tables()