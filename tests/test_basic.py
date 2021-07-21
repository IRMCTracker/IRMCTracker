import os
import inspect
from modules.database import insert_server, get_servers
from modules.config import Env


# print(insert_server('MegaWorld', 1311, 2502, '1.12.2 - 1.17', 'https://google.com'))
for server in get_servers():
    print(server['name'], server['current_players'])
