from os import getenv
from modules.config import get
from dotenv import load_dotenv
from distutils.util import strtobool

class Config:   
    class Channels:
        VC_1 = get('channels.top.vc-1')
        VC_2 = get('channels.top.vc-2')
        VC_3 = get('channels.top.vc-3')
        VC_4 = get('channels.top.vc-4')
        VC_5 = get('channels.top.vc-5')
        VC_6 = get('channels.top.vc-6')
        
        ALL = get('channels.total-vc')
        EMPTY = get('channels.zero-vc')
        HOURLY = get('channels.text-hourly')
        
        ADMIN = get('channels.admin')

    class Roles:
        DEFAULT = get('roles.default')
        
class Env:
    load_dotenv('storage/data/.env')
    
    DEBUG = bool(strtobool(getenv('DEBUG')))
    LOG_SQL = bool(strtobool(getenv('LOG_SQL')))

    TOKEN = getenv('DEBUG_TOKEN') if DEBUG else getenv('TOKEN')
    PREFIX = getenv('DEBUG_PREFIX') if DEBUG else getenv('PREFIX')
    
    DB_PATH = getenv('DB_PATH')
    CONFIG_PATH = getenv('CONFIG_PATH')
