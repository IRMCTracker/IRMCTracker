from modules.config import get

class Config:   
    class Channels:
        TOP_CHANNELS = get('channels.top')
        TOP_VOTED_CHANNELS = get('channels.top_voted')
        
        RECORD_CHANNEL = get('channels.record')
        
        ALL = get('channels.total-vc')
        EMPTY = get('channels.zero-vc')
        HOURLY = get('channels.text-hourly')
        
        ADMIN = get('channels.admin')

        ALERTS = get('channels.alerts')

        CACHE = get('channels.cache')

    class Roles:
        DEFAULT = get('roles.default')
