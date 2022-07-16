from modules.config import get

class Config:   
    GUILD_ID = get('guild-id')

    class Log:
        DISCORD_DEBUG = bool(get('log.discord-debug'))
        SQL_QUERIES = bool(get('log.sql-queries'))

    class Bot:
        DEBUG_ENABLED = bool(get('bot.debug.enabled'))
        TOKEN = get('bot.debug.token') if DEBUG_ENABLED else get('bot.token')
        PREFIX = get('bot.debug.prefix').split(",") if DEBUG_ENABLED else get('bot.prefix').split(",")
        HYPIXEL_KEY = get('bot.hypixel-key')

    class MySQL:
        USER = get('mysql.user')
        PASSWORD = get('mysql.password')
        DATABASE = get('mysql.database')
        HOST = get('mysql.host')
        PORT = get('mysql.port')
    
    class Channels:
        TOP_PLAYERS = get('channels.top-players')
        TOP_VOTED = get('channels.top-voted')
        
        RECORD = get('channels.record')
        
        ALL = get('channels.total-vc')
        EMPTY = get('channels.zero-vc')
        HOURLY = get('channels.hourly-chart')
        PIE = get('channels.pie-chart')
        
        ADMIN = get('channels.admin')

        ALERTS = get('channels.alerts')

        CACHE = get('channels.cache')

        MEMBERS = get('channels.members-count')
        SERVERS = get('channels.servers-count')
        VOTES = get('channels.votes-count')
        TRACKS = get('channels.tracks-count')

        TRACK_USAGE = get('channels.track-usage')
        PROFILE_USAGE = get('channels.profile-usage')
        SKIN_USAGE = get('channels.skin-usage')

    class Roles:
        DEFAULT = get('roles.default')
