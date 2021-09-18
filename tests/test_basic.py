"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from modules.database.models.vote import get_top_voted_servers
from peewee import DoesNotExist

from urllib.request import urlopen
import json

from modules.database import *
create_tables()
