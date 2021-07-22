from time import time

def replace_placeholders(string, placeholders):
    placeholders['%timestamp%'] = str(time())

    for placeholder in placeholders:
        string = string.replace('%' + placeholder + '%', str(placeholders[placeholder]))
    
    return string
    