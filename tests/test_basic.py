from modules.database import create_tables
from modules.tracker import MCTracker

create_tables()

t = MCTracker()
t.fetch_and_sort()

t.update_servers_in_database()