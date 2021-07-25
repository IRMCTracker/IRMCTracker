from .foundation import DB
from .queries import CREATE_SERVERS_TABLE, \
                     INSERT_SERVER, \
                     SELECT_SERVER_ALIKE_WITH_NAME, \
                     UPDATE_SERVER_WITH_NAME, \
                     SELECT_SERVER_WITH_NAME, \
                     SELECT_ALL_SERVERS, \
                     SELECT_ALL_SERVERS_ORDERED, \
                     SELECT_PLAYERS_COUNT, \
                     SELECT_ZERO_PLAYER_COUNT

from modules.utils import prefer_not_null

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


def update_server(name, current_players=None, top_players=None, latest_version=None, latest_latency=None, favicon_path=None, motd_path=None, info_path=None, discord=None):
    server = get_server(name)
    
    return DB.sql_execute(UPDATE_SERVER_WITH_NAME, placeholders={
        'name': name,
        'current_players': prefer_not_null(current_players, server['current_players']),
        'top_players': prefer_not_null(top_players, server['top_players']),
        'latest_version': prefer_not_null(latest_version, server['latest_version']),
        'latest_latency': prefer_not_null(latest_latency, server['latest_latency']),
        'favicon_path': prefer_not_null(favicon_path, server['favicon_path']),
        'motd_path': prefer_not_null(motd_path, server['motd_path']),
        'info_path': prefer_not_null(info_path, server['info_path']),
        'discord': prefer_not_null(discord, server['discord'] if server['discord'] else 'null')
    })


def get_server(name):
    return DB.sql_fetch(SELECT_SERVER_WITH_NAME, last=True, placeholders={
        'name': name
    })

@DB.fetch
def get_all_servers():
    return SELECT_ALL_SERVERS

@DB.fetch
def get_all_servers_sorted():
    return SELECT_ALL_SERVERS_ORDERED


def zero_player_servers_count():
    result = DB.sql_fetch(SELECT_ZERO_PLAYER_COUNT)
    print(result)
    print(dir(result))

    return 4

@DB.fetch_value
def all_players_count():
    return SELECT_PLAYERS_COUNT