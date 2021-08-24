from modules.config import Env
from peewee import MySQLDatabase

database = MySQLDatabase(Env.MYSQL_DATABASE, user=Env.MYSQL_USER, password=Env.MYSQL_PASSWORD,
                         host=Env.MYSQL_HOST, port=Env.MYSQL_PORT, charset='utf8mb4')

