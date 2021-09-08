from os import getenv
from modules.config import get
from dotenv import load_dotenv
from distutils.util import strtobool

class Config:   
    class Channels:
        TOP_CHANNELS = get('channels.top')
        RECORD_CHANNEL = get('channels.record')
        
        ALL = get('channels.total-vc')
        EMPTY = get('channels.zero-vc')
        HOURLY = get('channels.text-hourly')
        
        ADMIN = get('channels.admin')

        ALERTS = get('channels.alerts')

        CACHE = get('channels.cache')

    class Roles:
        DEFAULT = get('roles.default')
        
class Env:
    load_dotenv('storage/data/.env')
    
    DEBUG = bool(strtobool(getenv('DEBUG')))
    LOG_SQL = bool(strtobool(getenv('LOG_SQL')))
    LOG_DEBUG_DISCORD = bool(strtobool(getenv('LOG_DEBUG_DISCORD')))

    TOKEN = getenv('DEBUG_TOKEN') if DEBUG else getenv('TOKEN')
    PREFIX = getenv('DEBUG_PREFIX') if DEBUG else getenv('PREFIX')
    
    DB_PATH = getenv('DB_PATH')
    CONFIG_PATH = getenv('CONFIG_PATH')

    MYSQL_USER = getenv('MYSQL_USER')
    MYSQL_PASSWORD = getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = getenv('MYSQL_DATABASE')
    MYSQL_HOST = getenv('MYSQL_HOST')
    MYSQL_PORT = int(getenv('MYSQL_PORT'))

    HYPIXEL_KEY = getenv('HYPIXEL_KEY')