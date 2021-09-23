from discord import Embed, File
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown
from modules.tracker import get_servers
from modules.utils import *

class ServersCommand(Cog):
    """Servers command cog

    Shows all the servers and their players from db
    """

    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['allservers'])
    @cooldown(6, 60, BucketType.user)
    async def servers(self, ctx):
        """Sending all the sorted servers in an embed
        """

        servers = get_servers()
        banner = File('storage/static/banner.png', filename='banner.png')
        embed = Embed(title="📡 Servers List | لیست سرور ها", description='', color=0x673AB7, timestamp=get_utc())

        offline_servers = []
        i = 0
        for server in servers:
            if i == 0:
                prefix = '🥇'
            elif i == 1:
                prefix = '🥈'
            elif i == 2:
                prefix = '🥉'
            else:
                prefix = '🏅'

            if server.latest_latency == 0:
                offline_servers.append(server)
            else:
                embed.add_field(name=f"{prefix} {server.name}", value=f"👥 {server.current_players}", inline=True)

            i += 1

        for server in offline_servers:
            embed.add_field(name=f"🔴 {server.name}", value=f"👥 -", inline=True)

        embed.set_image(url='attachment://banner.png')

        embed.set_footer(text='Tracked by IRMCTracker')

        await ctx.send(ctx.author.mention, file=banner, embed=embed)
    
    @servers.error
    async def servers_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor servers ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336, timestamp=get_utc())
            await ctx.send(ctx.author.mention, embed=embed)

def setup(client):
    client.add_cog(ServersCommand(client))
