"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist
from modules.database import *

create_tables()

# 3 server bartar bar asas tedad vote

servers = get_servers()

for server in servers:
    try:
        server.votes_count = len(server.votes)
    # Excepts when server doesnt have any votes so we set it to 0
    except DoesNotExist:
        server.votes_count = 0

    
servers_sorted = sorted(servers, key=lambda x: x.votes_count, reverse=True)
for server in servers_sorted:
    print(server.name, server.votes_count)