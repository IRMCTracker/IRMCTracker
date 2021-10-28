from modules.database.basemodel import *
from .server import Server

from datetime import datetime, timedelta

class Records(BaseModel):
    id = PrimaryKeyField()
    players = IntegerField(null=True, default=0)
    latency = IntegerField(null=True, default=0)
    server_id = ForeignKeyField(Server, 'id', backref='records')
    created_at = DateTimeField()

    class Meta:
        table_name = 'records'

def get_all_records_count():
    try:
        return Records.select().count()
    except DoesNotExist:
        return 0

def add(server, players_count: int, latest_latency: int) -> bool:  
    Records.replace(
        players = players_count,
        server_id = server,
        latency = latest_latency,
        created_at = datetime.now()
    ).execute()

    return True

def get_server_records(server):
    return Records.select().where(Records.server_id == server & (Records.created_at > (datetime.now() - timedelta(days=7)).date()))
    

def get_highest_players(server) -> int:
    return Records.select(fn.MAX(Records.players)).where(Records.server_id == server).scalar()
