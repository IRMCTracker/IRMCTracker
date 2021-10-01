import os

from time import time

from datetime import datetime as dt

from modules.config import Config
from modules.tracker import MCTracker, get_servers, all_players_count, zero_player_servers_count, get_servers_by_record, get_servers_limit
from modules.database.models.records import get_highest_players
from modules.database.models.server_meta import get as get_meta
from modules.database.models.vote import get_top_voted_servers

from modules.utils import *

from discord.ext import tasks
from discord import File, Embed, Activity, ActivityType
from discord.ext.commands import Cog

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
    # END OF TRACKER TASKS

    async def send_chart(self):
        """Sending the chart to #hourly-chart channel
        """

        MCTracker().draw_chart()

        servers = get_servers()

        embed = Embed(title="⏰ Hourly Track", 
                        description=f"🥇 **{servers[0].name}** in the lead with **{servers[0].current_players}** Players", 
                        color=0x00D166, timestamp=get_utc())
        embed.set_footer(text=f"Tracked by IRMCTracker", icon_url="https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128")
        file = File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.HOURLY).send(
            file=file, embed=embed
        )

        os.remove('chart.png')
    
def setup(client):
    client.add_cog(TrackerTasks(client))
