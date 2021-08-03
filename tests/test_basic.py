"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from modules.database import *

create_tables()

print(remove_server(name='GharchCraft'))
for server in get_servers():
    print(server.name)



