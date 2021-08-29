from typing import Text
from modules.database.basemodel import *
from .server import Server

class ServerMeta(BaseModel):
    key = TextField()
    value = LongTextField()
    server_id = ForeignKeyField(Server, 'id', backref='meta')

    class Meta:
        table_name = 'servers_meta'
        indexes = (
            (("key", "server_id"), True),
        )
