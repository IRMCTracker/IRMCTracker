import datetime
from config import get
import matplotlib.pyplot as plt
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

    def get_name(self):
        return self.server_name

class MCTracker:
    def __init__(self):
        self.servers_config = get('servers')
        self.data = []
        self.is_fetched = False

    def fetch_all(self):        
        for server in self.servers_config:
            self.data.append(MCServer(server['name'], server['address']))
        
        self.is_fetched = True

        return self.data

    def sort_all(self):
        if not self.is_fetched:
            return print('You should exec MCTracker#fetch_all first!')
        
        self.data.sort(key=lambda x: x.get_online_players(), reverse=True)

        return self.data


    def separated_names_and_players(self):
        names = []
        players = []

        for server in self.data:
            name = server.get_name()
            names.append((name[:8] + '..') if len(name) > 8 else name)
            players.append(server.get_online_players())
            
        return {'names': names, 'players': players}

    def draw_chart(self, output_file='chart.png'):
        separated = self.separated_names_and_players()

        names = separated['names']
        players = separated['players']
        colors = ['lime','lime','green','green','darkgreen','darkgreen', 'gold', 'yellow', 'khaki', 'orangered', 'indianred', 'firebrick', 'firebrick']

        fig = plt.figure(figsize=(18,8))
        plt.bar(names, players, color=colors)
        plt.title(f"Iranian MineCraft Servers - {datetime.datetime.now():%Y-%m-%d %I:%M:%S}")
        plt.xlabel('Server Names', fontsize=8, labelpad=5)
        plt.ylabel('Players Count', fontsize=8, labelpad=5)
        plt.savefig(output_file)

        return output_file
    
    def zero_player_count(self):
        count = 0
        for server in self.data:
            if server.get_online_players() == 0:
                count += 1
        return count

    def all_player_count(self):
        total = 0
        for server in self.data:
            total += server.get_online_players()
        return total
