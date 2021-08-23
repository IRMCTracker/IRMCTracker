from os.path import exists

from discord import Embed, File
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown
from datetime import datetime
from modules.tracker import get_servers
from modules.database import get_server_like
from modules.utils import get_beautified_dt

class Track(Cog):
    """Track commands cog

    All the tracker commands for public users

    TODO:
        - Add a command for fetching custom domain/ip addresses
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
        embed = Embed(title="📡 Servers List | لیست سرور ها", description='', color=0x673AB7)

        offline_servers = []
        for server in servers:
            if server.latest_latency == 0:
                offline_servers.append(server)
            else:
                embed.add_field(name=f"🟢 {server.name}", value=f"👥 {server.current_players}", inline=True)

        for server in offline_servers:
            embed.add_field(name=f"🔴 {server.name}", value=f"👥 -", inline=True)

        embed.set_image(url='attachment://banner.png')

        embed.set_footer(text='Tracked at ' +   get_beautified_dt())

        await ctx.send(ctx.author.mention, file=banner, embed=embed)

    @command(aliases=['status','stats', 'server'])
    @cooldown(6, 60, BucketType.user)
    async def track(self, ctx, server=None):
        """Track command for getting information about servers
        """

        mention_msg = ctx.author.mention

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title='Dastoor vared shode motabar nist.', 
                                        description='Estefade dorost: ```.track [servername]\nMesal: .track madcraft```',
                                        color=0xF44336))

        server = get_server_like(server)

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title='Server vared shode vojood nadarad!',
                                        description='Ba dastoor zir tamami server haro bebinid ```.servers```',
                                        color=0xF44336))
        else:
            discord = server.discord if server.discord != 'null' else 'Not Set'

            if server.latest_latency == 0:
                embed = Embed(title=f"🔴 {server.name}", description='Server morede nazar shoma dar hale hazer offline hast : (', color=0xc62828)
                return await ctx.send(mention_msg, embed=embed)
            if server.motd_path == 'null' or not exists(server.motd_path):
                server.motd_path = 'storage/static/banner.png'
            
            embed=Embed(title="", color=0x1bd027)
            embed.set_author(name=f"💎 {server.name}")

            favicon = File(server.favicon_path, filename="image.png")

            # TODO REMOVE THIS LINE (forcing motd to default banner)
            server.motd_path = 'storage/static/banner.png'
            
            motd = File(server.motd_path, filename="motd.png")
            embed.set_thumbnail(url="attachment://image.png")

            embed.add_field(name="🌐 Address", value=server.address, inline=False)
            embed.add_field(name="👥 Online Players", value=server.current_players, inline=True)
            embed.add_field(name="🥇 Top Players Record", value=server.top_players, inline=True)
            embed.add_field(name="🔗 Discord", value=discord, inline=False)
            embed.add_field(name="📌 Version", value=server.latest_version, inline=True)
            embed.add_field(name="📡 Latency", value=f"{str(server.latest_latency)} ms", inline=True)
            #I don't check if it exists because it already exists in tempdata and injected in main loop before anyone execute any command
            if not self.bot.tempdata[server.address]["lastDowntime"] is None:
                final = datetime.now() - self.bot.tempdata[server.address]["lastDowntime"]
                final = final.total_seconds()
                thevalue = None
                if final >= 3600:
                    thevalue = f"Aprx {round(final/3600)} hour(s)"
                else:
                    thevalue = f"Aprx {round(final/60)} minute(s)"

                embed.add_field(name="\U0001f559 Uptime", value=thevalue, inline=True)
            embed.set_image(url="attachment://motd.png")
            await ctx.send(mention_msg, files=[favicon, motd], embed=embed)
        
    @track.error
    async def track_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor track ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336)
            await ctx.send(ctx.author.mention, embed=embed)
        

def setup(bot):
    bot.add_cog(Track(bot))
