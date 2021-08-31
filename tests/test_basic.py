"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist

from modules.database import server_meta, records, create_tables, Server, get_servers_by_record

from random import randrange


create_tables()

for s in get_servers_by_record():
    print(s.name + ' | ' + str(s.top_players))
