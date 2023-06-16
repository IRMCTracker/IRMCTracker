import os
from dotenv import load_dotenv

load_dotenv()

class Config:   
    GUILD_ID = int(os.getenv('GUILD_ID'))
    SERVER_OF_YEAR_ID = int(os.getenv('SERVER_OF_YEAR_ID'))

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
        PORT = int(os.getenv('MYSQL_PORT'))
    
    class Channels:
        TOP_PLAYERS = [int(i) for i in os.getenv('TOP_PLAYERS').split(", ")]
        TOP_VOTED = [int(i) for i in os.getenv('TOP_VOTED').split(", ")]
        
        RECORD = int(os.getenv('RECORD'))
        
        ALL = int(os.getenv('TOTAL_VC'))
        EMPTY = int(os.getenv('ZERO_VC'))
        HOURLY = int(os.getenv('HOURLY_CHART'))
        PIE = int(os.getenv('PIE_CHART'))
        
        ADMIN = int(os.getenv('ADMIN'))

        ALERTS = int(os.getenv('ALERTS'))

        CACHE = int(os.getenv('CACHE'))

        MEMBERS = int(os.getenv('MEMBERS_COUNT'))
        SERVERS = int(os.getenv('SERVERS_COUNT'))
        VOTES = int(os.getenv('VOTES_COUNT'))
        TRACKS = int(os.getenv('TRACKS_COUNT'))

        TRACK_USAGE = int(os.getenv('TRACK_USAGE'))
        PROFILE_USAGE = int(os.getenv('PROFILE_USAGE'))
        SKIN_USAGE = int(os.getenv('SKIN_USAGE'))

        SERVER_OF_YEAR_CHANNEL = int(os.getenv('SERVER_OF_YEAR'))

    class Roles:
        DEFAULT = int(os.getenv('DEFAULT_ROLE'))
