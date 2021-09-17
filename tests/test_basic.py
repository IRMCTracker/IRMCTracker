"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from modules.database.models.vote import get_top_voted_servers
from peewee import DoesNotExist

from modules.database import server_meta, records, create_tables, Server, get_servers_by_record

from random import randrange

from modules.database import *
create_tables()

