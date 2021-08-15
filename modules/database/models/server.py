from typing import Text
from modules.database.basemodel import *

class Server(BaseModel):
    id = PrimaryKeyField()
    name = CharField(150, unique=True)
    address = CharField(150, unique=True)
    discord = CharField(150, null=True)
    favicon_path = LongTextField(null=True)
    info_path = LongTextField(null=True)
    motd_path = LongTextField( null=True)
    latest_version = CharField(255, null=True)
    latest_latency = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    current_players = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    top_players = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'servers'
