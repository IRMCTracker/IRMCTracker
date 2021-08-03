from modules.config import Env
from peewee import SqliteDatabase

database = SqliteDatabase(Env.DB_PATH)

