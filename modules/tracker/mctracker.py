import datetime, time
import json
from time import sleep

from modules.database.trackerdb import *
from modules.database import records
from modules.utils import shortified, DomainInfo

from .mcserver import MCServer
import matplotlib.pyplot as plt

def update_server_database(server: MCServer, add_record: bool):
    db = server.fetch_server_from_db()

    if db is None:
        return

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
        gamemodes=json.dumps(server.get_gamemodes()),
        ip = resolve_info.get_ip(),
        country_code = resolve_info.get_country_code(),
        region = resolve_info.get_region()
    )

    # Add track record to database
    # WILL ONLY ADD EVERY 2 HOURS
    if add_record:
        records.add(db, current_players, latency)
    else:
        # Update last record if players are higher than highest record
        highest_players = get_highest_players(db.id)

        if current_players > highest_players:
            last_record = Records.select().where(Records.server_id == db.id).order_by(Records.id.desc()).get()
            last_record.players = current_players
            last_record.save()


class MCTracker:
    def __init__(self):
        self.all_servers = get_servers()
        self.is_fetched = False
        self.counter = 0

    def update_servers(self):  
        add_record = True if self.counter % 40 == 0 else False
        
        for server in self.all_servers:
            update_server_database(MCServer(server.name, server.address), add_record)

        self.counter += 1
        
        self.is_fetched = True

    def update_task(self):
        while True:
            start =  time.time()

            self.update_servers()

            end =  time.time()

            # Checking if fetching server took more than
            # 60 seconds we'll ignore sleep and go for another
            # round of fetching servers
            if (end - start) > 60:
                continue
            sleep(60)

    def draw_chart(self, output_file='chart.png'):
        names = []
        players = []
        for server in self.all_servers:
            # We wont show 0 player servers anymore
            if server.current_players != 0:
                names.append(shortified(server.name, 6, False))
                players.append(server.current_players)

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