from peewee import *
from modules.config import Env

database = SqliteDatabase(Env.DB_PATH)

class BaseModel(Model):
    class Meta:
        database = database

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False
