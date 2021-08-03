import asyncio
import datetime

from modules.database.trackerdb import *
from modules.utils import shortified

import matplotlib.pyplot as plt

from .mcserver import MCServer

class MCTracker():
    def __init__(self):
        self.all_servers = get_servers()
        self.mcservers = []
        self.is_fetched = False

    def fetch_servers(self):  
        self.mcservers.clear()

        for server in self.all_servers:
            self.mcservers.append(MCServer(server.name, server.address))
        
        self.is_fetched = True

        return self.mcservers
    
    def update_servers_database(self, update_motd=False):
        for server in self.mcservers:
            db = server.fetch_server_from_db()

            current_players = server.get_online_players()
            top_record = db.top_players

            if current_players > top_record:
                top_record = current_players

            update_server(
                name=server.get_name(),
                current_players=current_players, 
                top_players=top_record, 
                latest_version=server.get_version(), 
                latest_latency=server.get_latency(), 
                favicon_path=server.get_favicon_path(),
            )

            if update_motd:
                update_server(
                    name=server.get_name(),
                    motd_path=server.get_motd()
                )

    def update_task(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            self.fetch_servers()

            self.update_servers_database()

            asyncio.sleep(60)            

    def draw_chart(self, output_file='chart.png'):
        names = [shortified(server.name, 6) for server in self.all_servers]
        players = [server.current_players for server in self.all_servers]

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