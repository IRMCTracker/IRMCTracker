import discord

from time import time
import random, string
import timeago
from datetime import datetime as dt

def replace_placeholders(string, placeholders):
    placeholders['%timestamp%'] = str(time())

    for placeholder in placeholders:
        string = string.replace('%' + placeholder + '%', str(placeholders[placeholder]))
    
    return string

def random_string(len=16):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))

def get_beautified_dt():
    return f"{dt.now():%Y-%m-%d %I:%M:%S}"

def prefer_not_null(a, b):
    if a not in [None, 'null']:
        return a
    return b
    
def shortified(string, max_len=6) -> str:
    return (string[:max_len] + '..') if len(string) > max_len else string

def ago(date, locale='en_US'):
    return timeago.format(date, locale=locale)

def timestamp_ago(timestamp, locale='en_US'):
    return ago(dt.fromtimestamp(timestamp), locale)

def capitalize_address(address):
    return '.'.join([x.capitalize() for x in address.split('.')])


class Emojis:
    def __init__(self, emojis):
        self.emojis = emojis

    def get_emoji(self, name):
        return discord.utils.get(self.emojis, name=name)
