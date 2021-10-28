from modules.database.basemodel import *
from .server import Server

# This model is created website-site so we won't create it
# from our pov, do it if you need
class Vote(BaseModel):
    id = BigIntegerField(unique=True)
    username = CharField()
    server_id = BigIntegerField()
    created_at = TimestampField()
    updated_at = TimestampField()

    class Meta:
        table_name = 'votes'

def get_all_votes_count():
    try:
        return Vote.select().count()
    except DoesNotExist:
        return 0

def get_server_votes_count(server_id: int):
    try:
        return Vote.select().where(Vote.server_id == server_id).count()
    except DoesNotExist:
        return 0


def get_top_voted_servers(amount:int = 3):
    servers = Server.select()

    for server in servers:
        server.votes = get_server_votes_count(server.id)
        
    return sorted(servers, key=lambda x: x.votes, reverse=True)[:amount]