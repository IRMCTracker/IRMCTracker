from modules.config import Env
from peewee import SqliteDatabase
from .models import *

database = SqliteDatabase(Env.DB_PATH)
tables = [Server, Vote]

def create_tables():
    database.create_tables(tables)