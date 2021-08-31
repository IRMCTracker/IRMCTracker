"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist

from modules.database import server_meta, records, create_tables, Server

create_tables()

madcraft = Server.get(Server.name == 'MadCraft')
records.add(madcraft, 134, 5)
print(records.get_highest_players(madcraft))

