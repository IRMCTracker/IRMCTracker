from enum import unique
from modules.database.basemodel import *

class Server(BaseModel):
    id = PrimaryKeyField()
    name = CharField(150, unique=True)
    description = LongTextField(null=True)
    address = CharField(150, unique=True)
    ip = CharField(150, null=True)
    country_code = CharField(50, null=True)
    region = CharField(100, null=True)
    favicon_path = LongTextField(null=True)
    info_path = LongTextField(null=True)
    motd_path = LongTextField( null=True)
    gamemodes = LongTextField( null=True)
    latest_version = CharField(255, null=True)
    latest_latency = IntegerField(null=True, default=0)
    current_players = IntegerField(null=True, default=0)
    max_players = IntegerField(null=True, default=0)
    up_from = BigIntegerField(default=0)
    is_vip = BooleanField(default=False)
    channel_id = BigIntegerField(default=0)

    class Meta:
        table_name = 'servers'
