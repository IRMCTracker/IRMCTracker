from modules.config import CONFIG

def get_config():
    return CONFIG.get()

def path_to_array(string):
    return string.split('.')

def get(full_path: str):
    cfg = get_config()
    for path in path_to_array(full_path):
        cfg = cfg[path]

    return cfg
    