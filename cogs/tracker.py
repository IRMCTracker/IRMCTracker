import os
from datetime import datetime as dt

from modules.config import Config
from modules.tracker import MCTracker, get_all_servers_sorted, all_players_count, zero_player_servers_count
from modules.utils import shortified, get_beautified_dt

from discord.ext import tasks
from discord import File, Embed, Activity, ActivityType
from discord.ext.commands import Cog, command, has_role

class Tracker(Cog):
    """Doing all the automated tracking->discord tasks

    """

    def __init__(self, bot):
        self.bot = bot
        self.servers = get_all_servers_sorted()
    
    @tasks.loop(minutes=1)
    async def tracker_tick(self):
        """Main Tracker tick

        Main tick for sending hourly charts, updating activity and updating channels
        """

        minute = dt.now().minute

        self.servers = get_all_servers_sorted()

        # Every five minutes or hour
        if minute % 5 == 0 or minute == 0:
            # Every five minutes
            if minute % 5 == 0:
                await self.update_channels()
            # Every hour
            if minute == 0:
                await self.send_chart()

        await self.update_activity()
        
    async def update_activity(self):
        """Simply updating bot activity
        """

        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"{all_players_count()} players in {str(len(self.servers))} servers"
            )
        )

    async def send_chart(self):
        """Sending the chart to #hourly-chart channel
        """

        MCTracker().draw_chart()

        embed = Embed(title="Hourly Track", description=f"🥇 **{self.servers[0]['name']}** in the lead with **{self.servers[0]['current_players']}** Players", color=0x00D166) #creates embed
        embed.set_footer(text=f"IRMCTracker Bot - {get_beautified_dt()}")
        file = File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.HOURLY).send(
            file=file, embed=embed
        )

        os.remove('chart.png')

    async def update_channels(self):
        """Updating the channels with newly fetched data

        TODO:
            - Refactor this code (Can do it with a simple for loop)
        """
        await self.bot.get_channel(Config.Channels.VC_1).edit(
            name=f"🥇 {shortified(self.servers[0]['name'], 10)} [{self.servers[0]['current_players']}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_2).edit(
            name=f"🥇 {shortified(self.servers[1]['name'], 10)} [{self.servers[1]['current_players']}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_3).edit(
            name=f"🥈 {shortified(self.servers[2]['name'], 10)} [{self.servers[2]['current_players']}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_4).edit(
            name=f"🥈 {shortified(self.servers[3]['name'], 10)} [{self.servers[3]['current_players']}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_5).edit(
            name=f"🥉 {shortified(self.servers[4]['name'], 10)} [{self.servers[4]['current_players']}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_6).edit(
            name=f"🥉 {shortified(self.servers[5]['name'], 10)} [{self.servers[5]['current_players']}👥]"
        )

        await self.bot.get_channel(Config.Channels.ALL).edit(
            name=f"💎 All Players [{all_players_count()}👥]"
        )
        await self.bot.get_channel(Config.Channels.EMPTY).edit(
            name=f"📈 Empty Count [{zero_player_servers_count()}🔨]"
        )  

def setup(client):
    client.add_cog(Tracker(client))
