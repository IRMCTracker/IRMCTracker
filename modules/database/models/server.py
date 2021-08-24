from typing import Text
from modules.database.basemodel import *

class Server(BaseModel):
    id = PrimaryKeyField()
    name = CharField(150, unique=True)
    address = CharField(150, unique=True)
    discord = CharField(150, null=True)
    telegram = CharField(150, null=True)
    instagram = CharField(150, null=True)
    shop = CharField(150, null=True)
    website = CharField(150, null=True)
    favicon_path = LongTextField(null=True)
    info_path = LongTextField(null=True)
    motd_path = LongTextField( null=True)
    latest_version = CharField(255, null=True)
    latest_latency = IntegerField(null=True, default=0)
    current_players = IntegerField(null=True, default=0)
    top_players = IntegerField(null=True, default=0)
    up_from = BigIntegerField(default=0)
    channel_id = BigIntegerField(default=0)

    class Meta:
        table_name = 'servers'
