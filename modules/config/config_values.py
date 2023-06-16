import os
from dotenv import load_dotenv

load_dotenv()

class Config:   
    GUILD_ID = os.getenv('GUILD_ID')
    SERVER_OF_YEAR_ID = os.getenv('SERVER_OF_YEAR_ID')

    class Log:
        DISCORD_DEBUG = bool(os.getenv('LOG_DISCORD_DEBUG'))

    class Bot:
        TOKEN = os.getenv('BOT_TOKEN')
        PREFIX = os.getenv('BOT_PREFIX').split(",")
        HYPIXEL_KEY = os.getenv('HYPIXEL_KEY')

    class MySQL:
        USER = os.getenv('MYSQL_USER')
        PASSWORD = os.getenv('MYSQL_PASSWORD')
        DATABASE = os.getenv('MYSQL_DATABASE')
        HOST = os.getenv('MYSQL_HOST')
        PORT = os.getenv('MYSQL_PORT')
    
    class Channels:
        TOP_PLAYERS = os.getenv('TOP_PLAYERS').split(", ")
        TOP_VOTED = os.getenv('TOP_VOTED').split(", ")
        
        RECORD = os.getenv('RECORD')
        
        ALL = os.getenv('TOTAL_VC')
        EMPTY = os.getenv('ZERO_VC')
        HOURLY = os.getenv('HOURLY_CHART')
        PIE = os.getenv('PIE_CHART')
        
        ADMIN = os.getenv('ADMIN')

        ALERTS = os.getenv('ALERTS')

        CACHE = os.getenv('CACHE')

        MEMBERS = os.getenv('MEMBERS_COUNT')
        SERVERS = os.getenv('SERVERS_COUNT')
        VOTES = os.getenv('VOTES_COUNT')
        TRACKS = os.getenv('TRACKS_COUNT')

        TRACK_USAGE = os.getenv('TRACK_USAGE')
        PROFILE_USAGE = os.getenv('PROFILE_USAGE')
        SKIN_USAGE = os.getenv('SKIN_USAGE')

        SERVER_OF_YEAR_CHANNEL = os.getenv('SERVER_OF_YEAR')

    class Roles:
        DEFAULT = os.getenv('DEFAULT_ROLE')
