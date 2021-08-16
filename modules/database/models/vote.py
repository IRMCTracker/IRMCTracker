from modules.database.basemodel import *
from .server import Server

class Vote(BaseModel):
    user_id = BigIntegerField(unique=True)
    server_id = ForeignKeyField(Server, 'id', backref='votes')

    class Meta:
        table_name = 'votes'
