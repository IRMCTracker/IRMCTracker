from modules.config import get

class Config:   
    GUILD_ID = get('guild-id')
    
    class Channels:
        TOP_CHANNELS = get('channels.top_players')
        TOP_VOTED_CHANNELS = get('channels.top_voted')
        
        RECORD_CHANNEL = get('channels.record')
        
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

        TRACK_USAGE_CHANNEL = get('channels.track-usage')
        PROFILE_USAGE_CHANNEL = get('channels.profile-usage')
        SKIN_USAGE_CHANNEL = get('channels.skin-usage')

    class Roles:
        DEFAULT = get('roles.default')
