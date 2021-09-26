from modules.config import Config
from modules.database.models.records import get_highest_players
from modules.database.models.server_meta import get as get_meta
from modules.database.models.vote import get_top_voted_servers
from modules.database import get_servers

from modules.utils import *

from discord.ext import tasks
from discord import Embed
from discord.ext.commands import Cog


class TopServersTask(Cog):
    """Updating top servers channels task
    """

    def __init__(self, bot):
        self.bot = bot
        self.servers = get_servers()

        # Running top channels update task
        self.update_top_servers_task.start()

    @tasks.loop(minutes=1)
    async def update_top_servers_task(self):
        """Updating top players / top voted channels
        """
        await self.bot.wait_until_ready()
        
        await self.update_top_players_channels()
        await self.update_top_voted_channels()


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

def setup(client):
    client.add_cog(TopServersTask(client))
