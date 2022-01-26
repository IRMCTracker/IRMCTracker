from discord.errors import HTTPException
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

        # Running top channels update task
        self.update_top_voted_channels.start()
        self.update_top_players_channels.start()
    
    @tasks.loop(seconds=15)
    async def update_top_voted_channels(self):
        await self.bot.wait_until_ready()

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

            await self.edit_embed(server, messages[0])

            i += 1

    @tasks.loop(seconds=15)
    async def update_top_players_channels(self):
        await self.bot.wait_until_ready()

        i = 0
        servers = get_servers()

        for channel_id in Config.Channels.TOP_CHANNELS:
            channel = self.bot.get_channel(channel_id)
            messages = await channel.history(limit=1).flatten()

            server = servers[i]
            
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

            try:
                await self.edit_embed(server, messages[0])
            except HTTPException as e:
                get_logger().warn("HTTPException error occured")
                get_logger().warn("Exception: {}".format(type(e).__name__))
                get_logger().warn("Exception message: {}".format(e))


            i += 1

    def is_online(self, server):
        if server.latest_latency == 0 and server.current_players == 0:
            return False
        return True        

    async def edit_embed(self, server, msg):
        socials = []

        if get_meta(server, 'discord'):
            socials.append(f"{self.bot.emoji('discord')} [Discord]({get_meta(server, 'discord')})")
        if get_meta(server, 'telegram'):
            socials.append(f"{self.bot.emoji('telegram')} [Telegram](https://t.me/{str(get_meta(server, 'telegram')).replace('@','')})")
        if get_meta(server, 'instagram'):
            socials.append(f"{self.bot.emoji('instagram')} [Instagram](https://instagram.com/{get_meta(server, 'instagram')})")
        if get_meta(server, 'shop'):
            socials.append(f"{self.bot.emoji('shop')} [Shop]({get_meta(server, 'shop')})")
        if get_meta(server, 'website'):
            socials.append(f"{self.bot.emoji('web')} [Website]({get_meta(server, 'website')})")

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
        if server.ip != None and bool(get_meta(server, 'show-ip')):
            ip = f"( **{server.ip}** )"
        
        embed.add_field(name="「🌐」Address »", value=f"{capitalize_address(server.address)} {ip}", inline=False)
        embed.add_field(name="「👥」Online Players »", value=server.current_players, inline=True)
        embed.add_field(name="「🥇」Top Record »", value=get_highest_players(server), inline=True)
        embed.add_field(
            name='「📈」Uptime »',
            value=uptime, 
            inline=False
        )
        custom_version = get_meta(server, 'custom_version')
        embed.add_field(name="「📌」Version »", value=server.latest_version if custom_version == None else custom_version, inline=True)
        embed.add_field(name="「📡」Latency »", value=f"{str(server.latest_latency)} ms", inline=True)

        if server.country_code != None:
            embed.add_field(name="「🌎」Country »", value=f":flag_{str(server.country_code).lower()}: {server.region}", inline=False)

        if server.gamemodes != None:
            gamemodes_raw = json.loads(server.gamemodes)

            if len(gamemodes_raw) > 0:
                gamemodes_list = ["{} **{}** 「**{}**👥」".format(self.bot.emoji(str(gamemode['name']).lower()) or self.bot.emoji("barrier"),gamemode['name'], gamemode['players']) for gamemode in gamemodes_raw]
                gamemodes = '\n'.join(gamemodes_list)

                embed.add_field(
                    name=f"「🎮」Games Status »",
                    value=gamemodes,
                    inline=True
                )
        
        if len(socials) > 0:
            socials_message = '\n'.join(socials)

            embed.add_field(
                name=f"「{self.bot.emoji('people')}」Socials »", 
                value=socials_message, 
                inline=True
            )

        cache_channel = self.bot.get_channel(Config.Channels.CACHE)

        if server.favicon_path != None:
            try:
                file = await cache_channel.send(file=discord.File(server.favicon_path))
                image_url = file.attachments[0].url
                embed.set_thumbnail(url=image_url)
            except HTTPException as e:
                get_logger().warn("HTTPException error occured")
                get_logger().warn("Exception: {}".format(type(e).__name__))
                get_logger().warn("Exception message: {}".format(e))

        if server.motd_path != None:
            try:
                file = await cache_channel.send(file=discord.File(server.motd_path))
                image_url = file.attachments[0].url
                embed.set_image(url=image_url)
            except HTTPException as e:
                get_logger().warn("HTTPException error occured")
                get_logger().warn("Exception: {}".format(type(e).__name__))
                get_logger().warn("Exception message: {}".format(e))

        try:
            await msg.edit(content=None, embed=embed)
        except HTTPException as e:
            get_logger().warn("HTTPException error occured")
            get_logger().warn("Exception: {}".format(type(e).__name__))
            get_logger().warn("Exception message: {}".format(e))

def setup(client):
    client.add_cog(TopServersTask(client))
