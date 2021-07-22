from time import time
import random, string

def replace_placeholders(string, placeholders):
    placeholders['%timestamp%'] = str(time())

    for placeholder in placeholders:
        string = string.replace('%' + placeholder + '%', str(placeholders[placeholder]))
    
    return string

def random_string(len=16):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))
    