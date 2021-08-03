"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from modules.database import create_tables, get_servers_like, get_servers

create_tables()

for server in get_servers():
    print(server.name)
print(get_servers_like('C'))


