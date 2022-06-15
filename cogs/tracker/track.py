from discord import Embed, File
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown

from modules.config.config_values import Config
from modules.database import get_server_like, get_highest_players
from modules.database.models.server_meta import get as get_meta
from modules.utils import *

class TrackerGlobal(Cog):
    """Track command

    To get information of a specific server

    TODO:
        - Add a command for fetching custom domain/ip addresses
    """

    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['status','stats', 'server'])
    @cooldown(6, 60, BucketType.user)
    async def track(self, ctx, server=None):
        """Track command for getting information about servers
        """
        if ctx.channel.id != Config.Channels.TRACK_USAGE_CHANNEL:
            await ctx.message.add_reaction('❌')
            return

        mention_msg = ctx.author.mention

        if server is None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Dastoor vared shode motabar nist.", 
                                        description='Estefade dorost: ```.track [servername]\nMesal: .track madcraft```',
                                        color=0xF44336, timestamp=get_utc()))

        server = get_server_like(server)

        if server is None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Server vared shode vojood nadarad!",
                                        description='Ba dastoor zir tamami server haro bebinid ```.servers```',
                                        color=0xF44336, timestamp=get_utc()))
        else:
            if not is_online(server):
                embed = Embed(title=f"🔴 {server.name}", 
                                description=f"Server morede nazar shoma dar hale hazer offline hast : (\n\n⏰ Downtime: {timestamp_ago(abs(server.up_from))}", 
                                color=0xc62828, 
                                timestamp=get_utc())
                return await ctx.send(mention_msg, embed=embed)

            await self.send_embed(server, ctx)

    async def send_embed(self, server, ctx):
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
            description=f"{server.description if server.description is not None else ' '}",
            color=random_color(), 
            url = "https://mctracker.ir/server/{}".format(str(server.id)), 
            timestamp=get_utc()
        )

        embed.set_footer(
            text=f"Tracked By IRMCTracker",
            icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128'
        )


        ip = ""
        if server.ip is not None:
            if not bool(get_meta(server, 'show-ip')):
                ip = ""
            else:
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
        embed.add_field(name="「📌」Version »", value=server.latest_version if custom_version is None else custom_version, inline=True)
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

        files = []

        if server.favicon_path is not None:
            files.append(File(server.favicon_path, filename="image.png"))
            embed.set_thumbnail(url="attachment://image.png")

        if server.motd_path is not None:
            files.append(File(server.motd_path, filename="motd.png"))
            embed.set_image(url="attachment://motd.png")
        else:
            embed.set_image(url='storage/static/banner.png')
                        

        await ctx.send(ctx.author.mention, files=files, embed=embed)

    @track.error
    async def track_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor track ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336, timestamp=get_utc())
            await ctx.send(ctx.author.mention, embed=embed)
        

def setup(bot):
    bot.add_cog(TrackerGlobal(bot))
