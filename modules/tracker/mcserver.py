from mcstatus import MinecraftServer

class MCServer:
    def __init__(self, server_name, server_address, server_real_address = None):
        self.server_name = server_name
        self.server_address = server_address
        self.server_real_address = server_real_address
    
        self.server = self.lookup()
        
        self.status = self.get_status()

    def lookup(self):
        return MinecraftServer.lookup(self.server_address + ':25565')

    def get_status(self):
        try:
            data = self.server.status()
        except:
            data = None
        
        return data
    
    def get_online_players(self):
        return self.status.players.online if self.status != None else 0

    def get_latency(self):
        return self.status.latency if self.status != None else 0

    def get_name(self, shortified=False):
        name = self.server_name

        if shortified:
            return (name[:10] + '..') if len(name) > 10 else name
        return name

