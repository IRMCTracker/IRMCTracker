import re

import base64

import requests, os

from mcstatus import MinecraftServer

from modules.database import get_server
from modules.utils import *

import dns.resolver

class MCServer:
    def __init__(self, server_name, server_address):
        self.server_name = server_name
        self.server_address = server_address
    
        self.server = self.lookup()
        
        self.fetch_status()

    def lookup(self):
        return MinecraftServer.lookup(self._check_srv(self.server_address))
    
    def _check_srv(self, domain):
        try:
            srvInfo = {}
            srv_records=dns.resolver.query('_minecraft._tcp.'+domain, 'SRV')
            for srv in srv_records:
                srvInfo['host']     = str(srv.target).rstrip('.')
                srvInfo['port']     = srv.port
            address = srvInfo['host']
        except:
            address = domain
        
        return address

    def fetch_status(self):
        try:
            self.status = self.server.status()
        except:
            self.status = None
        
        return self.status
    
    def get_online_players(self):
        return self.status.players.online if self.status != None else 0
    
    def get_max_players(self):
        return self.status.players.max if self.status != None else 0

    def get_latency(self):
        return self.status.latency if self.status != None else 0

    def get_version(self):
        if self.status != None:
            return re.sub(r'§[A-Za-z1-9]', '', self.status.version.name)
        return None
            


    def get_name(self, shortified=False):
        name = self.server_name

        if shortified:
            return (name[:10] + '..') if len(name) > 10 else name
        return name
    
    def get_favicon_base64(self):
        return self.status.favicon if self.status != None else None

    def get_favicon_path(self):
        if self.status:
            data = str(self.status.favicon).replace('data:image/png;base64,', '')
            imgdata = base64.b64decode(data)
            filename = f"storage/cache/fav-{self.get_name()}.png"

            with open(filename, 'wb') as f:
                    f.write(imgdata)

            return filename
        else:
            return None

    def get_motd_path(self):
        if self.status:
            data = "http://status.mclive.eu/{}/{}/25565/banner.png".format(self.get_name(), self.server_address)
            filename = f"storage/cache/motd-{self.get_name()}.png"

            try:
                page = requests.get(data, timeout=6)
            except requests.exceptions.Timeout:
                return None

            if page.status_code != 200:
                return None
                
            with open(filename, 'wb') as f:
                f.write(page.content)

            return filename
        else:
            return None


    def fetch_server_from_db(self):
        return get_server(self.get_name())

    def get_description(self) -> str:
        return self.status.description if self.status != None else None