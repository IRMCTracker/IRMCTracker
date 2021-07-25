from modules.database import create_tables, get_all_servers_sorted

create_tables()

servers = get_all_servers_sorted()

names = [server['name'] for server in servers]
players = [server['current_players'] for server in servers]

print(names)
print(players)



