"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist
from modules.database import *
from modules.utils import UsernameToUUID
create_tables()

# 3 server bartar bar asas tedad vote

u = UsernameToUUID('Alijkgfdgdfgdf')
print(u.get_uuid() == '')