from typing import Text
from modules.database.basemodel import *

class Server(BaseModel):
    id = PrimaryKeyField()
    name = TextField(unique=True)
    address = TextField(unique=True)
    discord = TextField(null=True)
    favicon_path = LongTextField(null=True)
    info_path = LongTextField(null=True)
    motd_path = LongTextField(null=True)
    latest_version = LongTextField(null=True)
    latest_latency = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    current_players = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    top_players = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'servers'
