import base64
from os.path import isfile
from mcstatus import MinecraftServer

from modules.database import get_server
from modules.utils import random_string

class MCServer:
    def __init__(self, server_name, server_address, server_real_address = None):
        self.server_name = server_name
        self.server_address = server_address
        self.server_real_address = server_real_address
    
        self.server = self.lookup()
        
        self.fetch_status()

    def lookup(self):
        return MinecraftServer.lookup(self.server_address + ':25565')
    
    def fetch_status(self):
        try:
            self.status = self.server.status()
        except:
            self.status = None
        
        return self.status
    
    def get_online_players(self):
        return self.status.players.online if self.status != None else 0

    def get_latency(self):
        return self.status.latency if self.status != None else 0

    def get_version(self):
        return self.status.version.name if self.status != None else None

    def get_name(self, shortified=False):
        name = self.server_name

        if shortified:
            return (name[:10] + '..') if len(name) > 10 else name
        return name

    def get_favicon_path(self):
        if self.status:
            data = str(self.status.favicon).replace('data:image/png;base64,', '')
            imgdata = base64.b64decode(data)
            filename = 'storage/cache/' + random_string() + '.png'

            with open(filename, 'wb') as f:
                    f.write(imgdata)

            return filename
        else:
            return None

    def fetch_server_from_db(self):
        return get_server(self.get_name())

