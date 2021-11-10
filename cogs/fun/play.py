from urllib.parse import urlparse
import dns.asyncresolver

from discord import Embed
from discord.ext.commands import Cog, command, Bot, Context
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import cooldown
from discord.ext.commands.errors import CommandOnCooldown

from modules.config.config_values import Config
from modules.database.models.records import get_highest_players
from modules.database.models.server import Server
from modules.database.trackerdb import get_server_like
from modules.utils.functions import capitalize_address, get_utc, random_color, timestamp_ago
from modules.database.models.server_meta import get as get_meta


class Play(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['plei', 'plai', 'playy', 'pley', 'pleyy'])
    @command(aliases=['status', 'stats', 'server'])
    @cooldown(6, 60, BucketType.user)
    async def play(self, ctx: Context, server: str = None, user_name: str = None):
        """Track command for getting information about servers
        """
        if ctx.channel.id != Config.Channels.TRACK_USAGE_CHANNEL:
            await ctx.message.add_reaction('❌')
            return

        mention_msg = ctx.author.mention

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Dastoor vared shode motabar nist.",
                                                           description='Estefade dorost: ```.track [servername]\nMesal: .track madcraft```',
                                                           color=0xF44336, timestamp=get_utc()))

        server: Server = get_server_like(server)

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Server vared shode vojood nadarad!",
                                                           description='Ba dastoor zir tamami server haro bebinid ```.servers```',
                                                           color=0xF44336, timestamp=get_utc()))
        else:
            if not self.is_online(server):
                embed = Embed(title=f"🔴 {server.name}",
                              description=f"Server morede nazar shoma dar hale hazer offline hast : (\n\n⏰ Downtime: {timestamp_ago(abs(server.up_from))}",
                              color=0xc62828,
                              timestamp=get_utc())
                return await ctx.send(mention_msg, embed=embed)
            if server.ip == None:
                embed = Embed(title=f"🔴 {server.name}",
                              description=f"Server morede nazar shoma dar hale hazer dar dastras nist!",
                              color=0xc62828,
                              timestamp=get_utc())

                return await ctx.send(ctx.author.mention, embed=embed)
            await self.send_embed(server, ctx, user_name)

    def parse_address(self, address):
        tmp = urlparse("//" + address)
        if not tmp.hostname:
            raise ValueError("Invalid address '%s'" % address)
        return (tmp.hostname, tmp.port)

    async def lookup(self, address: str):
        host, port = self.parse_address(address)
        if port is None:
            port = 25565
            try:
                answers = await dns.asyncresolver.resolve(
                    "_minecraft._tcp." + host, "SRV")
                if len(answers):
                    answer = answers[0]
                    host = str(answer.target).rstrip(".")
                    port = int(answer.port)
            except Exception:
                pass

        return (host, port)

    def is_online(self, server: Server):
        if server.latest_latency == 0 and server.current_players == 0:
            return False
        return True

    async def send_embed(self, server: Server, ctx: Context, user_name: str):
        uptime = "-"
        if self.is_online(server):
            uptime = timestamp_ago(server.up_from)

        host, port = await self.lookup(server.ip)
        play_url = f"https://minecraft.js.org/?server={host}:{port}{'&nick=' + user_name  if user_name else '' }&proxy=production"

        embed = Embed(
            title=f"💎 {server.name}",
            description=f"[Play Dar Server]({play_url})",
            color=random_color(),
            url=f"{play_url}",
            timestamp=get_utc()
        )

        embed.set_footer(
            text=f"By IRMCTracker",
            icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128'
        )

        ip = f"( **{server.ip}** )"

        embed.add_field(
            name="「🌐」Address »", value=f"{capitalize_address(server.address)} {ip}", inline=False)
        embed.add_field(name="「👥」Online Players »",
                        value=server.current_players, inline=True)
        embed.add_field(name="「🥇」Top Record »",
                        value=get_highest_players(server), inline=True)
        embed.add_field(
            name='「📈」Uptime »',
            value=uptime,
            inline=False
        )
        embed.add_field(name="「📌」Version »",
                        value=server.latest_version, inline=True)
        embed.add_field(name="「📡」Latency »",
                        value=f"{str(server.latest_latency)} ms", inline=True)

        await ctx.send(ctx.author.mention, embed=embed)

    @play.error
    async def track_error(self, ctx: Context, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                          description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor play ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                          color=0xF44336, timestamp=get_utc())
            await ctx.send(ctx.author.mention, embed=embed)


def setup(bot: Bot):
    bot.add_cog(Play(bot))
