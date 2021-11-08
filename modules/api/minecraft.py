import requests
from modules.utils import *
from datetime import datetime

class Player:
    def __init__(self, username) -> None:
        self.username = username

        self.data = None

        self.BASE_URL = 'https://api.ashcon.app/mojang/v2/user/'
        self.BODY_BASE_URL = 'https://crafatar.com/renders/body/'
        self.HEAD_BASE_URL = 'https://crafatar.com/renders/head/'
        self.GET_ARGS = '?size=512&default=MHF_Steve&overlay'

        try:
            self.uuid = self.get_player_data()['uuid']
        except KeyError:
            self.uuid = ''

    def is_valid(self):
        return True if self.uuid != '' else False

    def get_body_image(self):
        return self.BODY_BASE_URL + self.uuid + self.GET_ARGS
    
    def get_head_image(self):
        return self.HEAD_BASE_URL + self.uuid + self.GET_ARGS
    
    def _fetch_player(self):
        return requests.get(
            url = self.BASE_URL + self.username,
        ).json()
    
    def get_player_data(self):
        if not self.data:
            self.data = self._fetch_player()
        return self.data

    def get_username_history(self):
        return self.get_player_data()['username_history']

    def get_other_usernames(self):
        return [x['username'] for x in self.get_username_history()][:-1]

    def get_created_at(self):
        return self.get_player_data()['created_at']
    
    def get_created_ago(self):
        if not self.get_created_at():
            return 'Not Shown'
        return f"{self.get_created_at()} ({timestamp_ago(datetime.strptime(self.get_created_at(), '%Y-%m-%d').timestamp())})"
    
    def get_uuid(self):
        return self.uuid