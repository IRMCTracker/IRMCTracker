from os import getenv
from dotenv import load_dotenv
from distutils.util import strtobool
        
class Env:
    load_dotenv('.env')
    
    DEBUG = bool(strtobool(getenv('DEBUG')))
    LOG_SQL = bool(strtobool(getenv('LOG_SQL')))
    LOG_DEBUG_DISCORD = bool(strtobool(getenv('LOG_DEBUG_DISCORD')))

    TOKEN = getenv('DEBUG_TOKEN') if DEBUG else getenv('TOKEN')
    PREFIX = getenv('DEBUG_PREFIX').split(",") if DEBUG else getenv('PREFIX').split(",")
    
    DB_PATH = getenv('DB_PATH')
    CONFIG_PATH = getenv('CONFIG_PATH')

    MYSQL_USER = getenv('MYSQL_USER')
    MYSQL_PASSWORD = getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = getenv('MYSQL_DATABASE')
    MYSQL_HOST = getenv('MYSQL_HOST')
    MYSQL_PORT = int(getenv('MYSQL_PORT'))

    HYPIXEL_KEY = getenv('HYPIXEL_KEY')