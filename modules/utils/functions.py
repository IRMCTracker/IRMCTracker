import discord

from random import randint
from time import time
import random, string
from datetime import datetime as dt


intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def timestamp_ago(timestamp: int, granularity=2):
    seconds = int(time() - timestamp)
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def random_color():
    return randint(0, 0xffffff)

def replace_placeholders(string, placeholders):
    placeholders['%timestamp%'] = str(time())

    for placeholder in placeholders:
        string = string.replace('%' + placeholder + '%', str(placeholders[placeholder]))
    
    return string

def random_string(len=16):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))

def get_utc():
    return dt.utcnow()

def get_beautified_dt():
    return f"{dt.now():%Y-%m-%d %I:%M:%S}"

def prefer_not_null(a, b):
    if a not in [None, 'null']:
        return a
    return b
    
def shortified(string, max_len=6, show_dots=True) -> str:
    return (string[:max_len] + ('..' if show_dots else '')
    ) if len(string) > max_len else string

def capitalize_address(address):
    return '.'.join([x.capitalize() for x in address.split('.')])

class Emojis:
    def __init__(self, emojis):
        self.emojis = emojis

    def get_emoji(self, name):
        return discord.utils.get(self.emojis, name=name)
