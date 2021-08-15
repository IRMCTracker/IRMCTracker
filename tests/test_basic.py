"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist
from modules.database import *
from modules.utils import UsernameToUUID
from modules.tracker import MCTracker
create_tables()

tracker = MCTracker()
tracker.fetch_servers()
tracker.update_servers_database()
