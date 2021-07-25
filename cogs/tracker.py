import os
from datetime import datetime as dt

from modules.config import Config, Env
from modules.tracker import MCTracker, get_all_servers_sorted, all_players_count, zero_player_servers_count
from modules.utils import shortified

from discord.ext import tasks
from discord import File, Embed, Activity, ActivityType
from discord.ext.commands import Cog, command, has_role

class Tracker(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers = get_all_servers_sorted()
    
    @tasks.loop(minutes=1)
    async def tracker_tick(self):
        minute = dt.now().minute

        self.servers = get_all_servers_sorted()

        if minute % 5 == 0 or minute == 0:
            if minute % 5 == 0:
                await self.update_channels()
            if minute == 0:
                await self.send_hourly()

        await self.update_activity()
        

    @command(has_role='root')
    @has_role('root')
    async def sendhourly(self,ctx):
        await self.send_hourly()

    @command(has_role='root')
    @has_role('root')
    async def updatedb(self,ctx):
        MCTracker().update_servers_database()

    @command()
    @has_role('root')
    async def updatechannels(self,ctx):
        await self.update_channels()

    async def update_activity(self):
        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"{all_players_count()} players in {str(len(self.servers))} servers"
            )
        )

    async def send_hourly(self):
        MCTracker().draw_chart()

        embed = Embed(title="Hourly Track", description=f"🥇 **{self.servers[0]['name']}** in the lead with **{self.servers[0]['current_players']}** Players", color=0x00D166) #creates embed
        embed.set_footer(text=f"IRMCTracker Bot - {dt.now():%Y-%m-%d %I:%M:%S}")
        file = File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.HOURLY).send(
            file=file, embed=embed
        )

        os.remove('chart.png')

    async def update_channels(self):
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
