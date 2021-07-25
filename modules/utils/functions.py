from time import time
import random, string
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
    
def shortified(string, max_len=6):
    return (string[:max_len] + '..') if len(string) > max_len else string