import os

from time import time

from datetime import datetime as dt

from modules.config import Config
from modules.tracker import MCTracker, get_servers, all_players_count, zero_player_servers_count, get_servers_by_record
from modules.database.models.records import get_highest_players
from modules.database.models.server_meta import get as get_meta
from modules.database.models.vote import get_top_voted_servers

from modules.utils import *

from discord.ext import tasks
from discord import File, Embed, Activity, ActivityType
from discord.ext.commands import Cog

class TrackerTasks(Cog):
    """Doing all the automated tracking->discord tasks

    """

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0
        self.servers = get_servers()

        # Running activity updating task
        self.update_activity_task.start()

        # Running top channels update task
        self.update_top_channels_task.start()

        # Running stats channels update task
        self.update_stats_channels_task.start()
        
        # Running main bot tick
        self.tracker_tick.start()
    
    # TRACKER TASKS
    @tasks.loop(seconds=15)
    async def update_activity_task(self):
        """Simply updating bot activity
        """

        await self.bot.wait_until_ready()

        players_count = all_players_count()
        servers_count = str(len(self.servers))

        if self.counter % 2 == 0:
            status_text = f"👥 {players_count} Players"
        else:
            status_text = f"💻 {servers_count} Servers"

        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=status_text
            )
        )

        self.counter += 1

    @tasks.loop(minutes=1)
    async def update_top_channels_task(self):
        """Updating top players / top voted channels
        """

        await self.bot.wait_until_ready()

        await self.update_top_players_channels()
        await self.update_top_voted_channels()

    @tasks.loop(minutes=1)
    async def update_stats_channels_task(self):
        """Updating stats voice channels
        """

        await self.bot.wait_until_ready()

        await self.bot.get_channel(Config.Channels.ALL).edit(
            name=f"💎・All「{all_players_count()}👥」"
        )
        await self.bot.get_channel(Config.Channels.EMPTY).edit(
            name=f"📈・Empty「{zero_player_servers_count()}🔨」"
        )  

        await self.update_records_text()

    @tasks.loop(minutes=1, reconnect=True)
    async def tracker_tick(self):
        """Main Tracker tick

        Main tick for sending hourly charts and registering uptime
        """

        await self.bot.wait_until_ready()

        # Fetching servers fresh data from database
        self.servers = get_servers()

        # Updating servers uptime status in database
        await self.register_uptime()

        # Every hour (1:00 , 2:00, ...)
        if dt.now().minute == 0:
            await self.send_chart()        
    # END OF TRACKER TASKS

    async def send_chart(self):
        """Sending the chart to #hourly-chart channel
        """

        MCTracker().draw_chart()

        embed = Embed(title="⏰ Hourly Track", 
                        description=f"🥇 **{self.servers[0].name}** in the lead with **{self.servers[0].current_players}** Players", 
                        color=0x00D166, timestamp=get_utc())
        embed.set_footer(text=f"Tracked by IRMCTracker")
        file = File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.HOURLY).send(
            file=file, embed=embed
        )

        os.remove('chart.png')

    async def update_records_text(self):
        channel = self.bot.get_channel(Config.Channels.RECORD_CHANNEL)
        messages = await channel.history(limit=1).flatten()

        embed = Embed(title="💎 Top Records | رکورد سرور های ایرانی",
                        description="لیست بالا ترین رکورد سرور های ایرانی بر اساس تعداد پلیر",
                        color=0x4CAF50, timestamp=get_utc())

        i = 0
        for server in get_servers_by_record():
            if i == 0:
                prefix = '🥇'
            elif i == 1:
                prefix = '🥈'
            elif i == 2:
                prefix = '🥉'
            else:
                prefix = '🏅'

            embed.add_field(
                name=f"{prefix} • {str(server.name).capitalize()}", 
                value=f"「 {get_highest_players(server)}👥 Players 」", 
                inline=False
            )

            i += 1

        embed.set_footer(text=f"Tracked by IRMCTracker")
        embed.set_image(url="https://cdn.discordapp.com/attachments/879304683590676482/879338350488748102/motd.png")

        await messages[0].edit(content=None, embed=embed)

    # TODO: Theres a lot of messy / duplicate code below here, Will refactor ASAP
    async def update_top_voted_channels(self):
        i = 0
        top_servers = get_top_voted_servers(len(Config.Channels.TOP_VOTED_CHANNELS))
        for channel_id in Config.Channels.TOP_VOTED_CHANNELS:

            channel = self.bot.get_channel(channel_id)
            messages = await channel.history(limit=1).flatten()

            server = top_servers[i]
            
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
                
            await channel.edit(
                name=f"{prefix}・{shortified(server.name, 9).capitalize()}「{server.votes}✌」"
            )

            socials = []

            if get_meta(server, 'discord'):
                socials.append(f"{self.bot.emoji('discord')} **➣** [Discord Link]({get_meta(server, 'discord')})")
            if get_meta(server, 'telegram'):
                socials.append(f"{self.bot.emoji('telegram')} **➣** [{get_meta(server, 'telegram')}](https://t.me/{str(get_meta(server, 'telegram')).replace('@','')})")
            if get_meta(server, 'instagram'):
                socials.append(f"{self.bot.emoji('instagram')} **➣** [@{get_meta(server, 'instagram')}](https://instagram.com/{get_meta(server, 'instagram')})")
            if get_meta(server, 'shop'):
                socials.append(f"{self.bot.emoji('shop')} **➣** [{get_meta(server, 'shop')}]({get_meta(server, 'shop')})")
            if get_meta(server, 'website'):
                socials.append(f"{self.bot.emoji('web')} **➣** [{get_meta(server, 'website')}]({get_meta(server, 'website')})")

            uptime = "-"
            if self.is_online(server):
                uptime = timestamp_ago(server.up_from)

            embed=Embed(
                title=f"💎 {server.name}",
                description=f"{server.description if server.description != None else ' '}", 
                color=random_color(), 
                url = "https://mctracker.ir/server/{}".format(str(server.id)), 
                timestamp=get_utc()
            )

            embed.set_footer(
                text=f"Tracked By IRMCTracker",
                icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128'
            )


            ip = ""
            if server.ip != None:
                ip = f"( **{server.ip}** )"
            
            embed.add_field(name="「🌐」 Address ►", value=f"{capitalize_address(server.address)} {ip}", inline=False)
            embed.add_field(name="「👥」 Online Players ►", value=server.current_players, inline=True)
            embed.add_field(name="「🥇」 Top Record ►", value=get_highest_players(server), inline=True)
            embed.add_field(
                name='「📈」 Uptime ►',
                value=uptime, 
                inline=False
            )
            embed.add_field(name="「📌」 Version ►", value=server.latest_version, inline=True)
            embed.add_field(name="「📡」 Latency ►", value=f"{str(server.latest_latency)} ms", inline=True)

            if server.country_code != None:
                embed.add_field(name="「🌎」 Country ►", value=f":flag_{str(server.country_code).lower()}: {server.region}", inline=False)

            socials_message = '\n'.join(socials)
            if len(socials) == 0:
                socials_message = 'No Socials Set'

            embed.add_field(
                name=f"「{self.bot.emoji('people')}」 Socials ►", 
                value=socials_message, 
                inline=False
            )

            if self.is_online(server):
                # Dealing with MOTD and ICON because cant edit images
                cache_channel = self.bot.get_channel(Config.Channels.CACHE)

                if server.favicon_path != None:
                    file = await cache_channel.send(file=discord.File(server.favicon_path))
                    image_url = file.attachments[0].url
                    embed.set_thumbnail(url=image_url)

                if server.motd_path != None:
                    file = await cache_channel.send(file=discord.File(server.motd_path))
                    image_url = file.attachments[0].url
                    embed.set_image(url=image_url)

                await messages[0].edit(content=None, embed=embed)


            i += 1

    async def update_top_players_channels(self):
        i = 0
        for channel_id in Config.Channels.TOP_CHANNELS:
            channel = self.bot.get_channel(channel_id)
            messages = await channel.history(limit=1).flatten()

            server = self.servers[i]
            
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
            else:
                players = server.current_players
                
            await channel.edit(
                name=f"{prefix}・{shortified(server.name, 9).capitalize()}「{players}👥」"
            )

            server.channel_id = channel_id
            server.save()

            socials = []

            if get_meta(server, 'discord'):
                socials.append(f"{self.bot.emoji('discord')} **➣** [Discord Link]({get_meta(server, 'discord')})")
            if get_meta(server, 'telegram'):
                socials.append(f"{self.bot.emoji('telegram')} **➣** [{get_meta(server, 'telegram')}](https://t.me/{str(get_meta(server, 'telegram')).replace('@','')})")
            if get_meta(server, 'instagram'):
                socials.append(f"{self.bot.emoji('instagram')} **➣** [@{get_meta(server, 'instagram')}](https://instagram.com/{get_meta(server, 'instagram')})")
            if get_meta(server, 'shop'):
                socials.append(f"{self.bot.emoji('shop')} **➣** [{get_meta(server, 'shop')}]({get_meta(server, 'shop')})")
            if get_meta(server, 'website'):
                socials.append(f"{self.bot.emoji('web')} **➣** [{get_meta(server, 'website')}]({get_meta(server, 'website')})")

            uptime = "-"
            if self.is_online(server):
                uptime = timestamp_ago(server.up_from)

            embed=Embed(
                title=f"💎 {server.name}",
                description=f"{server.description if server.description != None else ' '}", 
                color=random_color(), 
                url = "https://mctracker.ir/server/{}".format(str(server.id)), 
                timestamp=get_utc()
            )

            embed.set_footer(
                text=f"Tracked By IRMCTracker",
                icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128'
            )


            ip = ""
            if server.ip != None:
                ip = f"( **{server.ip}** )"
            
            embed.add_field(name="「🌐」 Address ►", value=f"{capitalize_address(server.address)} {ip}", inline=False)
            embed.add_field(name="「👥」 Online Players ►", value=server.current_players, inline=True)
            embed.add_field(name="「🥇」 Top Record ►", value=get_highest_players(server), inline=True)
            embed.add_field(
                name='「📈」 Uptime ►',
                value=uptime, 
                inline=False
            )
            embed.add_field(name="「📌」 Version ►", value=server.latest_version, inline=True)
            embed.add_field(name="「📡」 Latency ►", value=f"{str(server.latest_latency)} ms", inline=True)

            if server.country_code != None:
                embed.add_field(name="「🌎」 Country ►", value=f":flag_{str(server.country_code).lower()}: {server.region}", inline=False)

            socials_message = '\n'.join(socials)
            if len(socials) == 0:
                socials_message = 'No Socials Set'

            embed.add_field(
                name=f"「{self.bot.emoji('people')}」 Socials ►", 
                value=socials_message, 
                inline=False
            )

            if self.is_online(server):
                # Dealing with MOTD and ICON because cant edit images
                cache_channel = self.bot.get_channel(Config.Channels.CACHE)

                if server.favicon_path != None:
                    file = await cache_channel.send(file=discord.File(server.favicon_path))
                    image_url = file.attachments[0].url
                    embed.set_thumbnail(url=image_url)

                if server.motd_path != None:
                    file = await cache_channel.send(file=discord.File(server.motd_path))
                    image_url = file.attachments[0].url
                    embed.set_image(url=image_url)

                await messages[0].edit(content=None, embed=embed)


            i += 1

    def is_online(self, server):
        if server.latest_latency == 0:
            return False
        return True

    async def register_uptime(self):    
        """Refactored uptime registration system

        We have up_from field in database that changes to the timestamp that
        server starts to answer our requests so that we can calculate the time
        the server has been online
        Will set up_from field to a negative timestamp if server is offline in the latest check
        """
        alert_channel = self.bot.get_channel(Config.Channels.ALERTS)

        for server in self.servers:
            is_online = self.is_online(server)
            up_from_timestamp = server.up_from
            current_timestamp = round(time())

            embed = None
            
            # Means server is offline from last check in database
            if up_from_timestamp < 0:
                if is_online:
                    embed = Embed(
                        title=f"Server {server.name} online shod!",
                        description=f"\U0001f6a8 Server {server.name} lahazati pish online shod.\n\n⏰ Downtime: " + timestamp_ago(abs(server.up_from)),
                        color=0x00D166,
                        timestamp=get_utc()
                    )
                    server.up_from = current_timestamp

            # Means server is online from last check in database
            else:
                if not is_online:
                    embed = Embed(
                        title=f"❌ Server {server.name} offline shod!",
                        description=f"Server {server.name} lahazati pish az dastres kharej shod.\n\n⏰ Uptime: " + timestamp_ago(server.up_from),
                        color=0xff5757,
                        timestamp=get_utc()
                    )
                    server.up_from = -abs(current_timestamp)
            
            server.save()

            if embed != None:
                favicon = None
                if server.favicon_path:
                    favicon = File(server.favicon_path, filename="fav.png")
                    embed.set_thumbnail(url="attachment://fav.png")

                embed.set_footer(text=f"Tracked by IRMCTracker", icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=2048')

                await alert_channel.send(file=favicon,embed=embed)

    
def setup(client):
    client.add_cog(TrackerTasks(client))
