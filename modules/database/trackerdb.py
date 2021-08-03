from modules.database import Server, database

from modules.utils import prefer_not_null

def create_tables():
    database.create_tables([Server])

def remove_server(name):
    server = Server.get(Server.name == 'MCGO')
    server.delete()


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



def update_server(name, current_players=None, address=None, top_players=None, latest_version=None, latest_latency=None, favicon_path=None, motd_path=None, info_path=None, discord=None):
    server = get_server(name)
    
    return DB.sql_execute(UPDATE_SERVER_WITH_NAME, placeholders={
        'name': name,
        'current_players': prefer_not_null(current_players, server['current_players']),
        'address': prefer_not_null(address, server['address']),
        'top_players': prefer_not_null(top_players, server['top_players']),
        'latest_version': prefer_not_null(latest_version, server['latest_version']),
        'latest_latency': prefer_not_null(latest_latency, server['latest_latency']),
        'favicon_path': prefer_not_null(favicon_path, server['favicon_path']),
        'motd_path': prefer_not_null(motd_path, server['motd_path']),
        'info_path': prefer_not_null(info_path, server['info_path']),
        'discord': prefer_not_null(discord, server['discord'] if server['discord'] else 'null')
    })

def get_server(name):
    try:
        return Server.get(Server.name == name)
    except:
        return None

def get_servers_like(name):
    try:
        return Server.get(Server.name.contains(name))
    except:
        return None

def get_servers():
    return Server.select()

def zero_player_servers_count():
    result = DB.sql_fetch(SELECT_ZERO_PLAYER_COUNT, last=True)
    return result['zero_count']


def all_players_count():
    result = DB.sql_fetch(SELECT_PLAYERS_COUNT, last=True)
    return result['all_count']