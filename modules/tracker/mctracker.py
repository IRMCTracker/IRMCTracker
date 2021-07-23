import datetime

from numpy import logical_xor

from modules.config import Config
from modules.database import DB, update_server, get_server, get_all_servers

import matplotlib.pyplot as plt

from .mcserver import MCServer

class MCTracker(DB):
    def __init__(self):
        self.all_servers = get_all_servers()
        self.data = []
        self.is_fetched = False

    @staticmethod
    @DB.fetch
    def get_servers():
        return 'SELECT * FROM `servers`'

    def fetch_all(self):  
        self.data.clear()

        for server in self.all_servers:
            self.data.append(MCServer(server['name'], server['address']))
        
        self.is_fetched = True

        return self.data

    def sort_all(self):
        if not self.is_fetched:
            return print('You should exec MCTracker#fetch_all first!')
        
        self.data.sort(key=lambda x: x.get_online_players(), reverse=True)

        return self.data


    def fetch_and_sort(self):
        self.fetch_all()
        return self.sort_all()
    
    def update_servers_in_database(self):
        for server in self.data:
            db = server.fetch_server_from_db()

            current_players = server.get_online_players()
            top_record = db['top_players']

            if current_players > top_record:
                top_record = current_players

            update_server(
                server.get_name(),
                current_players, 
                top_record, 
                server.get_version(), 
                server.get_latency(), 
                server.get_favicon_path(), 
            )

    def update_servers_database_meta(self):
        for server in self.data:
            update_server(
                name=server.get_name(),
                favicon_path=server.get_favicon_path(), 
                motd_path=server.get_meta().get_motd_path(),
                # server.get_meta().get_info_path()
            )


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

        colors = []
        for player_count in players:
            if player_count > 120:
                color = 'lime'
            elif 120 > player_count > 80:
                color = 'green'
            elif 80 > player_count > 60:
                color = 'darkgreen'
            elif 60 > player_count > 50:
                color = 'gold'
            elif 50 > player_count > 40:
                color = 'yellow'
            elif 40 > player_count > 30:
                color = 'khaki'
            elif 30 > player_count > 20:
                color = 'orangered'
            elif 20 > player_count > 10:
                color = 'indianred'
            elif 10 > player_count:
                color = 'firebrick'
            
            colors.append(color)

        fig, ax = plt.subplots(figsize=(17,8))

        ax.bar(names, players, color=colors)
        plt.title(f"Iranian MineCraft Servers - {datetime.datetime.now():%Y-%m-%d %I:%M:%S}")
        plt.xlabel('Server Names', fontsize=8, labelpad=5)
        plt.ylabel('Players Count', fontsize=8, labelpad=5)

        for index,data in enumerate(players):
            x = index - 0.11
            if len(str(data)) == 3:
                x = index - 0.2

            plt.text(x=x , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=12))


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
