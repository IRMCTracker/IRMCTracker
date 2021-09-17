from os import getenv, walk
from confuse import Configuration
from .env_values import Env
from collections import defaultdict

CONFIG = Configuration('IRMCTracker', __name__)
CONFIG.set_file(getenv('CONFIG_PATH'))
CONFIG = CONFIG.get()

LANGUAGES = {}

# Loading lang  files
for path, subdirs, files in walk(Env.LANG_DIR):
    for name in files:
        if name.endswith('.yml'):
            lang_name = name[:-4]
            full_path = path + name

            lang = Configuration('Langauage-' + lang_name, __name__)
            lang.set_file(full_path)

            LANGUAGES[lang_name] = lang.get()

def get_path(full_path: str, cfg):
    for path in full_path.split('.'):
        cfg = cfg[path]

    return cfg

def get(path):
    return get_path(path, CONFIG)

def get_lang(path, locale=Env.DEFAULT_LANG):
    try:
        return get_path(path, LANGUAGES[locale])
    except KeyError:
        return None