import confuse

config = confuse.Configuration('IRMCTracker', __name__)
config.set_file('config.yml')


def get_config():
    return config.get()

def path_to_array(string):
    return string.split('.')

def get(full_path: str):
    cfg = get_config()
    for path in path_to_array(full_path):
        cfg = cfg[path]

    return cfg
