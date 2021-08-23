"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist
from modules.database import *
from modules.utils import *
from modules.tracker import MCTracker
create_tables()

madcraft = get_server('MadCraft')
eog = get_server('EOG')

print(timestamp_ago(madcraft.up_from))