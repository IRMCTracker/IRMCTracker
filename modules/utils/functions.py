import discord

from random import randint
from time import time
import random, string
import datetime
from datetime import datetime as dt
import arabic_reshaper
from bidi.algorithm import get_display
from os import sep
import uuid

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def humanize_number(value, significant_digits=3, strip_trailing_zeros=True):
    """
    Adaption of humanize_numbers_fp that will try to print a given number of significant digits, but sometimes more or
    less for easier reading.

    Examples:
    humanize_number(6666666, 2) = 6.7M
    humanize_number(6000000, 2) = 6M
    humanize_number(6000000, 2, strip_trailing_zeros=False) = 6.0M
    humanize_number(.666666, 2) = 0.67
    humanize_number(.0006666, 2) = 670µ
    """
    from math import log10, floor

    powers = [10 ** x for x in (12, 9, 6, 3, 0, -3, -6, -9)]
    human_powers = ['T', 'B', 'M', 'K', '', 'm', u'µ', 'n']
    is_negative = False
    suffix = ''

    if not isinstance(value, float):
        value = float(value)
    if value < 0:
        is_negative = True
        value = abs(value)
    if value == 0:
        decimal_places = max(0, significant_digits - 1)
    elif .001 <= value < 1:  # don't humanize these, because 3.0m can be interpreted as 3 million
        decimal_places = max(0, significant_digits - int(floor(log10(value))) - 1)
    else:
        p = next((x for x in powers if value >= x), 10 ** -9)
        i = powers.index(p)
        value = value / p
        before = int(log10(value)) + 1
        decimal_places = max(0, significant_digits - before)
        suffix = human_powers[i]

    return_value = ("%." + str(decimal_places) + "f") % value
    if is_negative:
        return_value = "-" + return_value
    if strip_trailing_zeros and '.' in return_value:
        return_value = return_value.rstrip('0').rstrip('.')

    return return_value + suffix

def timestamp_ago(timestamp: int, granularity=2):
    seconds = int(time() - int(timestamp))
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

def replace_placeholders(text, placeholders):
    placeholders['%timestamp%'] = str(time())

    for placeholder in placeholders:
        text = text.replace('%' + placeholder + '%', str(placeholders[placeholder]))
    
    return text

def random_string(length=16):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def get_utc():
    return dt.now(datetime.timezone.utc)

def to_persian(text):
    return get_display(arabic_reshaper.reshape(text))

def get_beautified_dt():
    return f"{dt.now():%Y-%m-%d %I:%M:%S}"

def prefer_not_null(a, b):
    if a not in [None, 'null']:
        return a
    return b
    
def shortified(text, max_len=6, show_dots=True) -> str:
    return (text[:max_len] + ('..' if show_dots else '')
    ) if len(text) > max_len else text

def capitalize_address(address):
    return '.'.join([x.capitalize() for x in address.split('.')])

def random_cache_file(ext):
    return "storage{}data{}cache{}{}.{}".format(sep, sep, sep, uuid.uuid4(), ext)

def get_medal_emoji(index):
    if index == 0:
        prefix = '🥇'
    elif index == 1:
        prefix = '🥈'
    elif index == 2:
        prefix = '🥉'
    else:
        prefix = '🏅'

    return prefix

def get_random_color():
    return randint(0, 0xffffff)

def is_online(server):
    if server.latest_latency == 0 and server.current_players == 0:
        return False
    return True

class Emojis:
    def __init__(self, emojis):
        self.emojis = emojis

    def get_emoji(self, name):
        return discord.utils.get(self.emojis, name=name)