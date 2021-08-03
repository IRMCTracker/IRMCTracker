from modules.database.basemodel import *

class Server(BaseModel):
    address = CharField(unique=True)
    current_players = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    discord = CharField(null=True)
    favicon_path = CharField(null=True)
    info_path = CharField(null=True)
    latest_latency = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    latest_version = CharField(null=True)
    motd_path = CharField(null=True)
    name = CharField(unique=True)
    top_players = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'servers'
