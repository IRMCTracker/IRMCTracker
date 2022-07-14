from peewee import MySQLDatabase
from modules.config import Config

database = MySQLDatabase(Config.MySQL.DATABASE, user=Config.MySQL.USER, password=Config.MySQL.PASSWORD,
                         host=Config.MySQL.HOST, port=Config.MySQL.PORT, charset='utf8mb4')

