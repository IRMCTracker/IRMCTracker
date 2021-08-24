"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist
from modules.database import *
from modules.utils import *
from modules.tracker import MCTracker
from modules.api.hypixel import HypixelPlayer
create_tables()

p = HypixelPlayer('Alijk')
print(p.get_status())
