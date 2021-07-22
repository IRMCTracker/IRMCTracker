from .foundation import DB
from .queries import CREATE_SERVERS_TABLE, \
                     INSERT_SERVER, \
                     SELECT_SERVER_ALIKE_WITH_NAME, \
                     UPDATE_SERVER_WITH_NAME, \
                     SELECT_SERVER_WITH_NAME

@DB.execute
def create_tables():
    return [
        CREATE_SERVERS_TABLE
    ]

def insert_server(name, address, current_players=0, top_players=0, latest_version='null', latest_latency=0, favicon_path='null', motd_path='null', info_path='null', discord='null'):
    return DB.sql_execute(INSERT_SERVER, placeholders={
        'name': name,
        'address': address,
        'current_players': current_players,
        'top_players': top_players,
        'latest_version': latest_version,
        'latest_latency': latest_latency,
        'favicon_path': favicon_path,
        'motd_path': motd_path,
        'info_path': info_path,
        'discord': discord
    })

def get_servers_like(name):
    return DB.sql_fetch(SELECT_SERVER_ALIKE_WITH_NAME, placeholders={
        'name': name
    })


def update_server(name, current_players=0, top_players=0, latest_version='null', latest_latency=0, favicon_path='null', motd_path='null', info_path='null', discord='null'):
    latest_version = 'null' if latest_version == None else latest_version
    favicon_path = 'null' if favicon_path == None else favicon_path

    return DB.sql_execute(UPDATE_SERVER_WITH_NAME, placeholders={
        'name': name,
        'current_players': current_players,
        'top_players': top_players,
        'latest_version': latest_version,
        'latest_latency': latest_latency,
        'favicon_path': favicon_path,
        'motd_path': motd_path,
        'info_path': info_path,
        'discord': discord
    })

def get_server(name):
    return DB.sql_fetch(SELECT_SERVER_WITH_NAME, last=True, placeholders={
        'name': name
    })

@DB.fetch
def get_all_servers():
    return 'SELECT * FROM `servers`'