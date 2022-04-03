from modules.database import database
from modules.database.models import *
from modules.database.models.records import get_highest_players
from modules.utils import prefer_not_null

from peewee import fn

tables = [Server, Records, DiscordVote, ServerMeta, Player]

def create_tables():
    database.create_tables(tables)

def remove_server(name):
    server = Server.get(Server.name == name)
    return server.delete_instance()

def insert_server(name, address):
    server = Server(name=name, address=address, up_from=0)
    return server.save()

def update_server(name, current_players=None, address=None, latest_version=None, latest_latency=None, 
                    favicon_path=None, motd_path=None, info_path=None, max_players=None, ip=None, country_code=None, region=None, gamemodes=None):
    old_server = get_server(name=name)
    
    server = Server.update(
        current_players = prefer_not_null(current_players, old_server.current_players),
        max_players = prefer_not_null(max_players, old_server.max_players),
        address = prefer_not_null(address, old_server.address),
        latest_version = prefer_not_null(latest_version, old_server.latest_version),
        latest_latency = prefer_not_null(latest_latency, old_server.latest_latency),
        favicon_path = prefer_not_null(favicon_path, old_server.favicon_path),
        motd_path = prefer_not_null(motd_path, old_server.motd_path),
        info_path = prefer_not_null(info_path, old_server.info_path),
        gamemodes = prefer_not_null(gamemodes, old_server.gamemodes),
        ip = prefer_not_null(ip, old_server.ip),
        country_code = prefer_not_null(country_code, old_server.country_code),
        region = prefer_not_null(region, old_server.region)
    ).where(Server.name == name)
    
    return server.execute()

def get_server(name):
    try:
        return Server.get(Server.name == name)
    except:
        return None

def get_server_like(name):
    try:
        return Server.get(Server.name.startswith(name))
    except:
        return None

def get_servers():
    return Server.select().order_by(Server.current_players.desc(), Server.up_from.desc())

def get_servers_limit(limit: int):
    return Server.select().order_by(Server.current_players.desc()).limit(limit)

def get_servers_by_record():
    servers = Server.select()
    sorted_list = []

    for server in servers:
        server.top_players = get_highest_players(server) or 0
        sorted_list.append(server)

    sorted_list.sort(key=lambda x: x.top_players, reverse=True)

    return sorted_list

def zero_player_servers_count():
    result = Server.select().where(Server.current_players == 0)
    return len(result)

def all_players_count():
    return Server.select(fn.SUM(Server.current_players)).scalar()
    