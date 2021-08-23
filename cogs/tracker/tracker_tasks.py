import os

from time import time

from datetime import datetime as dt

from modules.config import Config
from modules.tracker import MCTracker, get_servers, all_players_count, zero_player_servers_count
from modules.utils import *

from discord.ext import tasks
from discord import File, Embed, Activity, ActivityType
from discord.ext.commands import Cog

from art import text2art

class TrackerTasks(Cog):
    """Doing all the automated tracking->discord tasks

    """

    def __init__(self, bot):
        self.bot = bot
        self.servers = get_servers()
    
    @tasks.loop(minutes=1)
    async def tracker_tick(self):
        """Main Tracker tick

        Main tick for sending hourly charts, updating activity and updating channels
        """

        minute = dt.now().minute

        self.servers = get_servers()

        # Registering update and downtime events of a server in tempdata
        await self.register_uptime(self.servers)

        await self.update_top_text()

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

        embed = Embed(title="Hourly Track", description=f"🥇 **{self.servers[0].name}** in the lead with **{self.servers[0].current_players}** Players", color=0x00D166) #creates embed
        embed.set_footer(text=f"IRMCTracker Bot - {get_beautified_dt()}")
        file = File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.HOURLY).send(
            file=file, embed=embed
        )

        os.remove('chart.png')

    async def update_top_text(self):
        i = 0
        for channel_id in Config.Channels.TOP_CHANNELS:
            channel = self.bot.get_channel(channel_id)
            message = await channel.history(limit=1).flatten()[0]

            server = self.servers[i]

            discord = server.discord if server.discord != 'null' else 'Not Set'
            telegram = server.telegram if server.telegram != 'null' else 'Not Set'

            uptime = timestamp_ago(server.up_from)

            embed=Embed(title="", color=0x1bd027)
            embed.set_author(name=f"💎 {server.name}")

            favicon = File(server.favicon_path, filename="image.png")

            server.motd_path = 'storage/static/banner.png'
            motd = File(server.motd_path, filename="motd.png")
            embed.set_thumbnail(url="attachment://image.png")

            embed.add_field(name="🌐 Address ►", value=server.address, inline=False)
            embed.add_field(name="👥 Online Players ►", value=server.current_players, inline=True)
            embed.add_field(name="🥇 Top Players Record ►", value=server.top_players, inline=True)
            embed.add_field(name='📈 Uptime ►',
                description=uptime, 
                inline=False)
            embed.add_field(name="📌 Version ►", value=server.latest_version, inline=True)
            embed.add_field(name="📡 Latency ►", value=f"{str(server.latest_latency)} ms", inline=True)
            embed.add_field(name="🔗 Discord ►", value=discord, inline=False)
            embed.add_field(name="🔗 Telegram ►", value=telegram, inline=False)

            embed.set_image(url="attachment://motd.png")
            await message.edit(content=None, files=[favicon, motd], embed=embed)

            
            i += 1
    async def update_channels(self):
        """Updating the channels with newly fetched data
        """

        i = 0
        for channel_id in Config.Channels.TOP_CHANNELS:
            channel = self.bot.get_channel(channel_id)
            
            server = self.servers[i]
            name = shortified(server.name, 6).capitalize()

            players = server.current_players
            
            if i == 0:
                prefix = '🥇'
            elif i == 1:
                prefix = '🥈'
            elif i == 2:
                prefix = '🥉'
            else:
                prefix = '🏅'

            if not self.is_online(server):
                prefix = '❌'
                players = '-'

            await channel.edit(
                name=f"{prefix}︲{text2art(name, 'monospace')}「{players}👥」"
            )
            i += 1

        await self.bot.get_channel(Config.Channels.ALL).edit(
            name=f"💎 All Players 「{all_players_count()}👥」"
        )
        await self.bot.get_channel(Config.Channels.EMPTY).edit(
            name=f"📈 Empty Count 「{zero_player_servers_count()}🔨」"
        )  

    def is_online(self, server):
        if server.latest_latency == 0:
            return False
        return True

    async def register_uptime(self, servers):    
        """Refactored uptime registration system

        We have up_from field in database that changes to the timestamp that
        server starts to answer our requests so that we can calculate the time
        the server has been online
        Will set up_from field to 0 if server is offline in the latest check
        """        
        alert_channel = self.bot.get_channel(Config.Channels.ALERTS)

        for server in servers:
            is_online = self.is_online(server)
            up_from_timestamp = server.up_from
            current_timestamp = round(time())

            embed = None
            
            # Means server is offline from last check in database
            if up_from_timestamp == 0:
                if is_online:
                    embed = Embed(
                        title=f"Server {server.name} online shod!",
                        description=f"\U0001f6a8 Server {server.name} lahazati pish online shod.",
                        color=0x00D166
                    )
                    server.up_from = current_timestamp

            # Means server is online from last check in database
            else:
                if not is_online:
                    embed = Embed(
                        title=f"❌ Server {server.name} offline shod!",
                        description=f"Server {server.name} lahazati pish az dastres kharej shod.",
                        color=0xff5757
                    )
                    server.up_from = 0
            
            server.save()

            if embed != None:
                favicon = None
                if server.favicon_path:
                    favicon = File(server.favicon_path, filename="fav.png")
                    embed.set_thumbnail(url="attachment://fav.png")

                embed.set_footer(text=f"IRMCTracker Bot - {get_beautified_dt()}", icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=2048')

                await alert_channel.send(file=favicon,embed=embed)

    


def setup(client):
    client.add_cog(TrackerTasks(client))
