import enum
import confuse

config = confuse.Configuration('IRMCTracker', __name__)
config.set_file('config/config.yml')

def get_config():
    return config.get()

def path_to_array(string):
    return string.split('.')

def get(full_path: str):
    cfg = get_config()
    for path in path_to_array(full_path):
        cfg = cfg[path]

    return cfg


class Config:
    class Bot:
        TOKEN = get('bot.token')
        PREFIX = get('bot.prefix')
    
    class Channels:
        VC_1 = get('channels.top.vc-1')
        VC_1 = get('channels.top.vc-2')
        VC_1 = get('channels.top.vc-3')
        VC_1 = get('channels.top.vc-4')
        VC_1 = get('channels.top.vc-5')
        VC_1 = get('channels.top.vc-6')
        
        ALL = get('channels.total-vc')
        EMPTY = get('channels.zero-vc')
        HOURLY = get('channels.text-hourly')

    class Roles:
        DEFAULT = get('roles.default')
        
    SERVERS = get('servers')
    