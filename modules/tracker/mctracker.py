import datetime
from time import sleep

from modules.database.trackerdb import *
from modules.database import records
from modules.utils import shortified, DomainInfo

from .mcserver import MCServer

class MCTracker():
    def __init__(self):
        self.all_servers = get_servers()
        self.mcservers = []
        self.is_fetched = False
        self.counter = 0

    def fetch_servers(self):  
        self.mcservers.clear()

        for server in self.all_servers:
            s = MCServer(server.name, server.address)
            self.mcservers.append(s)

        self.is_fetched = True

        return self.mcservers
    
    def update_servers_database(self, update_motd=False):
        add_record = True if self.counter % 40 == 0 else False
        self.counter += 1

        for server in self.mcservers:
            db = server.fetch_server_from_db()

            resolve_info = DomainInfo(db.address)

            current_players = server.get_online_players()
            max_players = server.get_max_players()
            latency = server.get_latency()

            update_server(
                name=server.get_name(),
                current_players=current_players, 
                max_players=max_players,
                latest_version=server.get_version(), 
                latest_latency=latency, 
                favicon_path=server.get_favicon_path(),
                motd_path=server.get_motd_path(),
                ip = resolve_info.get_ip(),
                country_code = resolve_info.get_country_code(),
                region = resolve_info.get_region()
            )

            # Add track record to database
            # WILL CHECK TO ONLY ADD EVERY 2 HOURS
            if add_record:
                records.add(db, current_players, latency)

            if update_motd:
                update_server(
                    name=server.get_name(),
                    motd_path=server.get_motd()
                )

    def update_task(self):
        while True:
            self.fetch_servers()

            self.update_servers_database()

            sleep(60)      

    def draw_chart(self, output_file='chart.png'):
        import matplotlib.pyplot as plt
        
        names = [shortified(server.name, 6, False) for server in self.all_servers]
        players = [server.current_players for server in self.all_servers]

        colors = []
        for player_count in players:
            if player_count >= 150:
                color = 'lime'
            elif 150 > player_count >= 100:
                color = 'darkgreen'
            elif 100 > player_count >= 80:
                color = 'mediumseagreen'
            elif 80 > player_count >= 60:
                color = 'orange'
            elif 60 > player_count >= 40:
                color = 'yellow'
            elif 40 > player_count >= 30:
                color = 'darkkhaki'
            elif 30 > player_count >= 20:
                color = 'orangered'
            elif 20 > player_count >= 10:
                color = 'firebrick'
            elif 10 > player_count:
                color = 'brown'

            colors.append(color)

        fig, ax = plt.subplots(figsize=(17,8))

        ax.bar(names, players, color=colors)
        plt.title(f"[IR] MineCraft Servers - {datetime.datetime.now():%Y-%m-%d %I:%M:%S}")
        plt.xlabel('Servers', fontsize=8, labelpad=5)
        plt.ylabel('Players', fontsize=8, labelpad=5)

        for index,data in enumerate(players):
            x = index - 0.11
            if len(str(data)) == 3:
                x = index - 0.2
            plt.text(x=x , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=12))

        plt.savefig(output_file)

        plt.close(fig)
        
        return output_file