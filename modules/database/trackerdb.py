from modules.database import Server, Vote, database
from modules.utils import prefer_not_null

from peewee import fn

tables = [Server, Vote]

def create_tables():
    database.create_tables(tables)

def remove_server(name):
    server = Server.get(Server.name == name)
    return server.delete_instance()

def insert_server(name, address, current_players=0, top_players=0, latest_version='null', latest_latency=0,
                    favicon_path='null', motd_path='null', info_path='null', discord='null'):
    server = Server(name=name, address=address, current_players=current_players,
                        top_players=top_players, latest_version=latest_version,
                        latest_latency=latest_version, favicon_path=favicon_path, motd_path=motd_path,
                        info_path=info_path, discord=discord)
    return server.save()



def update_server(name, current_players=None, address=None, top_players=None, latest_version=None, latest_latency=None, 
                    favicon_path=None, motd_path=None, info_path=None, discord=None):
    old_server = get_server(name=name)
    
    server = Server.update(
        current_players = prefer_not_null(current_players, old_server.current_players),
        address = prefer_not_null(address, old_server.address),
        top_players = prefer_not_null(top_players, old_server.top_players),
        latest_version = prefer_not_null(latest_version, old_server.latest_version),
        latest_latency = prefer_not_null(latest_latency, old_server.latest_latency),
        favicon_path = prefer_not_null(favicon_path, old_server.favicon_path),
        motd_path = prefer_not_null(motd_path, old_server.motd_path),
        info_path = prefer_not_null(info_path, old_server.info_path),
        discord = prefer_not_null(discord, old_server.discord)
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
    return Server.select().order_by(Server.current_players.desc())

def get_servers_by_record():
    return Server.select().order_by(Server.top_players.desc())

def zero_player_servers_count():
    result = Server.select().where(Server.current_players == 0)
    return len(result)


def all_players_count():
    return Server.select(fn.SUM(Server.current_players)).scalar()
    