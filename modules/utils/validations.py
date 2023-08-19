import re
from discord import Message
from urllib.parse import urlparse

def has_link(message):
    # Define a list of domains to ignore
    ignored_domains = ["mctracker.ir", "forum.mctracker.ir"]

    regex = re.compile(
        r'(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    match = regex.search(message)
    if match:
        url = match.group(0)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        # Check if the domain is in the list of ignored domains
        if domain in ignored_domains:
            return False

    return match is not None

def has_discord_link(message):
    regex = re.compile(
    r'(https?://)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com/invite)/.+[a-z]', re.IGNORECASE)

    return regex.search(message) is not None

def message_has_mentions(message: Message):
    if message.mentions:
        return True
    return False