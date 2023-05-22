import os

from discord import File, Embed
from discord.ext import tasks
from discord.ext.commands import Cog

from modules.config import Config
from modules.tracker import get_servers
from modules.utils import *

from modules.utils import shortified
import matplotlib.pyplot as plt

class TrackerTasks(Cog):
    """Doing all the automated tracking->discord tasks

    """

    def __init__(self, bot):
        self.bot = bot
        
        # Running main bot tick
        self.tracker_tick.start()

    @tasks.loop(minutes=1, reconnect=True)
    async def tracker_tick(self):
        """Main Tracker tick

        Main tick for sending hourly charts and registering uptime
        """

        await self.bot.wait_until_ready()

        # Every hour (1:00 , 2:00, ...)
        if dt.now().minute == 0:
            await self.send_chart()

    async def send_chart(self):
        """Sending the chart to #hourly-chart channel
        """

        self.draw_chart()

        servers = get_servers()

        embed = Embed(title="⏰ Hourly Track", 
                        description=f"🥇 **{servers[0].name}** in the lead with **{servers[0].current_players}** Players", 
                        color=0x00D166, timestamp=get_utc())
        embed.set_footer(text=f"Tracked by IRMCTracker", icon_url="https://mctracker.ir/img/logo.png")
        file = File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.HOURLY).send(
            file=file, embed=embed
        )

        os.remove('chart.png')
    
    def draw_chart(self, output_file='chart.png'):
        names = []
        players = []
        for server in get_servers():
            # We wont show 0 player servers anymore
            if server.current_players != 0:
                names.append(shortified(server.name, 6, False))
                players.append(server.current_players)

        colors = []
        for player_count in players:
            if player_count >= 120:
                color = 'lime'
            elif 120 > player_count >= 90:
                color = 'darkgreen'
            elif 90 > player_count >= 75:
                color = 'mediumseagreen'
            elif 75 > player_count >= 50:
                color = 'orange'
            elif 50 > player_count >= 40:
                color = 'yellow'
            elif 40 > player_count >= 25:
                color = 'darkkhaki'
            elif 25 > player_count >= 15:
                color = 'orangered'
            elif 15 > player_count >= 5:
                color = 'firebrick'
            elif 5 > player_count:
                color = 'brown'

            colors.append(color)

        fig, ax = plt.subplots(figsize=(17,8))

        ax.bar(names, players, color=colors)
        plt.title(f"IRAN MineCraft Servers - {datetime.now():%Y-%m-%d %I:%M:%S}")
        plt.xlabel('Servers', fontsize=8, labelpad=5)
        plt.ylabel('Players Border', fontsize=8, labelpad=5)

        for index,data in enumerate(players):
            x = index - 0.11
            if len(str(data)) == 3:
                x = index - 0.2
            plt.text(x=x , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=12))

        plt.savefig(output_file)

        plt.cla()
        plt.clf()
        plt.close()
        
        return output_file

def setup(client):
    client.add_cog(TrackerTasks(client))
