import requests

from modules.config import Config
from modules.utils import *

class HypixelPlayer:
    def __init__(self, username) -> None:
        self.username = username
        self.uuid = UsernameToUUID(username).get_uuid()        

    def is_valid(self):
        return True if self.uuid != '' else False
    
    def _fetch_player(self):
        return requests.get(
            url = "https://api.hypixel.net/player",
            params = {
                "key": Config.Bot.HYPIXEL_KEY,
                "name": self.username
            }
        ).json()
    
    def _fetch_status(self):
        return requests.get(
            url = "https://api.hypixel.net/status",
            params = {
                "key": Config.Bot.HYPIXEL_KEY,
                "uuid": self.uuid
            }
        ).json()['session']

    def get_player(self):
        self.data = self._fetch_player()
        try:
            if not self.data['player'] or self.data['success'] == False:
                return None
            self.data['status'] = self._fetch_status()
            return self.data
        except KeyError:
            return None