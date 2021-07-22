from modules.database import insert_server, get_all_servers, create_tables
from modules.tracker import MCServer
from modules.config import Config

from mcstatus import MinecraftServer
from modules.tracker import MCTracker
from modules.utils import get_logger


# Database Seeder
# create_tables()
# for server in Config.SERVERS:
#     insert_server(server['name'], server['address'])

# get_logger('Debug').debug('Hi Test Message')

get_logger().debug('Test Message')