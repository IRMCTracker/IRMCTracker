"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist
from modules.database import *
from modules.utils import *
from modules.tracker import MCTracker
create_tables()

t = 'hub.madcraft.ir'

up = -1629793000
print(timestamp_ago(abs(up)))