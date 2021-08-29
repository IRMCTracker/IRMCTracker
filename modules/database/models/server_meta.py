from modules.database.basemodel import *
from .server import Server

class ServerMeta(BaseModel):
    key = LongTextField()
    value = LongTextField()
    server_id = ForeignKeyField(Server, 'id', backref='votes')

    class Meta:
        table_name = 'servers_meta'
        indexes = (
            (("key", "server_id"), True),
        )
