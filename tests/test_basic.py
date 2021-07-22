from modules.database import insert_server, get_all_servers, create_tables
from modules.tracker import MCServer
from modules.config import Config

from mcstatus import MinecraftServer
from modules.tracker import MCTracker


# Database Seeder
# create_tables()
# for server in Config.SERVERS:
#     insert_server(server['name'], server['address'])

tracker = MCTracker()

tracker.fetch_and_sort()

tracker.update_servers_in_database()