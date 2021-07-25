from modules.database import create_tables, DB

create_tables()

names = [server['name'] for server in DB.sql_fetch('SELECT name FROM servers')]
players = [server['current_players'] for server in DB.sql_fetch('SELECT current_players FROM servers')]
print(names)
print(players)



