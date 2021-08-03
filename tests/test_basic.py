"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from modules.database import *
servers = get_servers()

create_tables()

print(servers[0].name)
for server in servers:
    print(server.name + ' | ' + str(server.current_players) + ' | ' + str(server.top_players))



