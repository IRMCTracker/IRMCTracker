from logging import info
from modules.database import Server, database

from modules.utils import prefer_not_null

def create_tables():
    database.create_tables([Server])

def remove_server(name):
    server = Server.get(Server.name == name)
    return server.delete_instance()


def insert_server(name, address, current_players=0, top_players=0, latest_version='null', latest_latency=0, favicon_path='null', motd_path='null', info_path='null', discord='null'):
    server = Server(name=name, address=address, current_players=current_players,
                        top_players=top_players, latest_version=latest_version,
                        latest_latency=latest_version, favicon_path=favicon_path, motd_path=motd_path,
                        info_path=info_path, discord=discord)
    return server.save()



def update_server(name, current_players=None, address=None, top_players=None, latest_version=None, latest_latency=None, favicon_path=None, motd_path=None, info_path=None, discord=None):
    server = get_server(name)
    
    server.current_players = prefer_not_null(current_players, server['current_players']),
    server.address = prefer_not_null(address, server['address']),
    server.top_players = prefer_not_null(top_players, server['top_players']),
    server.latest_version = prefer_not_null(latest_version, server['latest_version']),
    server.latest_latency = prefer_not_null(latest_latency, server['latest_latency']),
    server.favicon_path = prefer_not_null(favicon_path, server['favicon_path']),
    server.motd_path = prefer_not_null(motd_path, server['motd_path']),
    server.info_path = prefer_not_null(info_path, server['info_path']),
    server.discord = prefer_not_null(discord, server['discord'] if server['discord'] else 'null')

    return server.save()

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