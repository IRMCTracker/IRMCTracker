from nextcord.errors import HTTPException
from modules.config import Config
from modules.database.models.records import get_highest_players
from modules.database.models.server_meta import get as get_meta
from modules.database.models.vote import get_top_voted_servers
from modules.database import get_servers

from modules.utils import *

from nextcord.ext import tasks
from nextcord import Embed
from nextcord.ext.commands import Cog


def log_http_exception(e):
    get_logger().warn("HTTPException error occured")
    get_logger().warn("Exception: {}".format(type(e).__name__))
    get_logger().warn("Exception message: {}".format(e))

class TopServersTask(Cog):
    """Updating top servers channels task
    """

    def __init__(self, bot):
        self.bot = bot
        self.TOP_PLAYERS_CHANNELS = []
        self.TOP_VOTED_CHANNELS = []

        # Running top channels update task
        self.update_top_channels.start()
    
    async def load_top_channels(self):
        async def add_channel(channel_id, where):
            channel = self.bot.get_channel(channel_id)
            message = (await channel.history(limit=1).flatten())[0]

            data = {
                "id": channel_id,
                "object": channel,
                "message": message
            }

            where.append(data)

        for channel_id in Config.Channels.TOP_CHANNELS:
            await add_channel(channel_id, self.TOP_PLAYERS_CHANNELS)

        for channel_id in Config.Channels.TOP_VOTED_CHANNELS:
            await add_channel(channel_id, self.TOP_VOTED_CHANNELS)

    @tasks.loop(minutes=1)
    async def update_top_channels(self):
        await self.bot.wait_until_ready()
        
        # Will be only running at the first time
        if len(self.TOP_VOTED_CHANNELS) == 0:
            await self.load_top_channels()

        await self.update_top_voted_channels()
        await self.update_top_players_channels()

    async def update_top_voted_channels(self):

        i = 0
        top_servers = get_top_voted_servers(len(Config.Channels.TOP_VOTED_CHANNELS))

        for top_channel in self.TOP_VOTED_CHANNELS:
            server = top_servers[i]
            
            prefix = get_medal_emoji(i) if is_online(server) else '❌'

            await top_channel["object"].edit(
                name=f"{prefix}・{shortified(server.name, 9).capitalize()}「{server.votes}✌」"
            )

            await self.edit_embed(server, top_channel["message"])

            i += 1

    async def update_top_players_channels(self):
        i = 0
        servers = get_servers()

        for top_channel in self.TOP_PLAYERS_CHANNELS:
            server = servers[i]
            
            prefix = get_medal_emoji(i)

            if not is_online(server):
                prefix = '❌'
                players = '-'
            else:
                players = server.current_players
                
            await top_channel["object"].edit(
                name=f"{prefix}・{shortified(server.name, 9).capitalize()}「{players}👥」"
            )

            server.channel_id = top_channel["id"]
            server.save()

            try:
                await self.edit_embed(server, top_channel["message"])
            except HTTPException as e:
                log_http_exception(e)

            i += 1

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
        if is_online(server):
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
        if server.ip is not None and bool(get_meta(server, 'show-ip')):
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

        if server.country_code is not None:
            embed.add_field(name="「🌎」Country »", value=f":flag_{str(server.country_code).lower()}: {server.region}", inline=False)

        if server.gamemodes is not None:
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

        if server.favicon_path is not None:
            try:
                file = await self.bot.CACHE_CHANNEL.send(file=nextcord.File(server.favicon_path))
                image_url = file.attachments[0].url
                embed.set_thumbnail(url=image_url)
            except HTTPException as e:
                log_http_exception(e)

        if server.motd_path is not None:
            try:
                if is_online(server):
                    file = await self.bot.CACHE_CHANNEL.send(file=nextcord.File(server.motd_path))
                else:        
                    file = await self.bot.CACHE_CHANNEL.send(file=nextcord.File('storage/static/banner.png'))
                image_url = file.attachments[0].url
                embed.set_image(url=image_url)
            except HTTPException as e:
                log_http_exception(e)

        try:
            await msg.edit(content=None, embed=embed)
        except HTTPException as e:
            log_http_exception(e)


def setup(client):
    client.add_cog(TopServersTask(client))
