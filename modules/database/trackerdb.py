from .foundation import DB
from .queries import CREATE_SERVERS_TABLE, INSERT_SERVER

@DB.execute
def create_tables():
    return [
        CREATE_SERVERS_TABLE
    ]

def insert_server(name, current_players, top_players, latest_version, discord):
    return DB.sql_execute(INSERT_SERVER, placeholders={
        'name': name,
        'current_players': current_players,
        'top_players': top_players,
        'latest_version': latest_version,
        'discord': discord
    })

@DB.fetch
def get_servers():
    return 'SELECT * FROM `servers`'