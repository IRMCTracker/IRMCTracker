from peewee import *
from modules.database.foundation import database

class BaseModel(Model):
    class Meta:
        database = database