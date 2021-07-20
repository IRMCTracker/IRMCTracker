import os
import discord
from config import Config
from mcserver import MCTracker
from datetime import datetime as dt
from discord.ext import commands, tasks

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracker = MCTracker()

        self.fetch_and_sort()

    def fetch_and_sort(self):
        self.tracker.fetch_all()
        self.sorted_servers = self.tracker.sort_all()
    
    @tasks.loop(minutes=1)
    async def tracker_tick(self):
        minute = dt.now().minute

        if minute % 5 == 0 or minute == 0:
            self.fetch_and_sort()

            if minute % 5 == 0:
                await self.update_channels()
            if minute == 0:
                await self.send_hourly()

        await self.update_activity()

    @commands.command()
    @commands.has_role('root')
    async def sendhourly(self,ctx):
        self.fetch_and_sort()

        await self.send_hourly()

    @commands.command()
    @commands.has_role('root')
    async def updatechannels(self,ctx):
        await self.update_channels()



    async def update_activity(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.tracker.all_player_count()} players in {str(len(Config.SERVERS))} servers"
            )
        )

    async def send_hourly(self):
        self.tracker.draw_chart()

        embed = discord.Embed(title="Hourly Track", description=f"🥇 **{self.sorted_servers[0].get_name()}** in the lead with **{self.sorted_servers[0].get_online_players()}** Players", color=0x00D166) #creates embed
        embed.set_footer(text=f"IRMCTracker Bot - {dt.now():%Y-%m-%d %I:%M:%S}")
        file = discord.File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.Hourly).send(
            file=file, embed=embed
        )

        os.remove('chart.png')

    async def update_channels(self):
        self.tracker.fetch_all()
        self.sorted_servers = self.tracker.sort_all()

        await self.bot.get_channel(Config.Channels.VC_1).edit(
            name=f"🥇 {self.sorted_servers[0].get_name()} [{self.sorted_servers[0].get_online_players()}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_2).edit(
            name=f"🥇 {self.sorted_servers[1].get_name()} [{self.sorted_servers[1].get_online_players()}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_3).edit(
            name=f"🥈 {self.sorted_servers[2].get_name()} [{self.sorted_servers[2].get_online_players()}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_4).edit(
            name=f"🥈 {self.sorted_servers[3].get_name()} [{self.sorted_servers[3].get_online_players()}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_5).edit(
            name=f"🥉 {self.sorted_servers[4].get_name()} [{self.sorted_servers[4].get_online_players()}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_6).edit(
            name=f"🥉 {self.sorted_servers[5].get_name()} [{self.sorted_servers[5].get_online_players()}👥]"
        )

        await self.bot.get_channel(Config.Channels.ALL).edit(
            name=f"💎 All Players [{self.tracker.all_player_count()}👥]"
        )
        await self.bot.get_channel(Config.Channels.EMPTY).edit(
            name=f"📈 Empty Count [{self.tracker.zero_player_count()}🔨]"
        )  

def setup(client):
    client.add_cog(Tracker(client))
