from os import getenv, walk
from confuse import Configuration
from .env_values import Env

CONFIG = Configuration('IRMCTracker', __name__)
CONFIG.set_file('config.yml')
CONFIG = CONFIG.get()

def get_path(full_path: str, cfg):
    for path in full_path.split('.'):
        cfg = cfg[path]

    return cfg

def get(path):
    return get_path(path, CONFIG)