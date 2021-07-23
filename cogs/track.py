from os.path import exists

from discord import Embed, File
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown

from modules.tracker import MCServer, get_all_servers
from modules.database import get_servers_like
from modules.utils import get_beautified_dt

class Track(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(aliases=['allservers'])
    @cooldown(6, 60, BucketType.user)
    async def servers(self, ctx):
        servers = get_all_servers()
        banner = File('storage/static/banner.png', filename='banner.png')
        embed = Embed(title="📡 Servers List | لیست سرور ها", description='', color=0x673AB7)
        for server in servers:
            embed.add_field(name=server['name'], value=f"👥 {server['current_players']}", inline=True)

        embed.set_image(url='attachment://banner.png')

        embed.set_footer(text='Tracked at ' +   get_beautified_dt())

        await ctx.send(file=banner, embed=embed)

    @command(aliases=['status','stats'])
    @cooldown(6, 60, BucketType.user)
    async def track(self, ctx, server=None):
        mention_msg = ctx.author.mention

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title='Dastoor vared shode motabar nist.', 
                                        description='Estefade dorost: ```.track [servername]\nMesal: .track madcraft```',
                                        color=0xF44336))

        servers_alike = get_servers_like(server)

        if len(servers_alike) == 0:
            return await ctx.send(mention_msg, embed=Embed(title='Server vared shode vojood nadarad!',
                                        description='Ba dastoor zir tamami server haro bebinid ```.servers```',
                                        color=0xF44336))
        elif len(servers_alike) > 1:
            alike_names = []
            [alike_names.append(server['name']) for server in servers_alike]

            return await ctx.send(mention_msg, embed=Embed(title='Server morede nazar peida nashod!',
                                        description='Shayad manzooretoon yeki az in hast: **' + ' | '.join(alike_names) + '**',
                                        color=0xcddc39))
        elif len(servers_alike) == 1:
            server = servers_alike[0]
            discord = server['discord'] if server['discord'] != 'null' else 'Not Set'

            if server['favicon_path'] == 'null' or not exists(server['favicon_path']):
                embed = Embed(title=f"🔴 {server['name']}", description='Server morede nazar shoma dar hale hazer offline hast : (', color=0xc62828)
                return await ctx.send(mention_msg, embed=embed)
            if server['motd_path'] == 'null' or not exists(server['motd_path']):
                server['motd_path'] = 'storage/static/banner.png'
            
            embed=Embed(title="", color=0x1bd027)
            embed.set_author(name=f"💎 {server['name']}")

            favicon = File(server['favicon_path'], filename="image.png")
            motd = File(server['motd_path'], filename="motd.png")
            embed.set_thumbnail(url="attachment://image.png")

            embed.add_field(name="🌐 Address", value=server['address'], inline=False)
            embed.add_field(name="👥 Online Players", value=server['current_players'], inline=True)
            embed.add_field(name="🥇 Top Players Record", value=server['top_players'], inline=True)
            embed.add_field(name="🔗 Discord", value=discord, inline=False)
            embed.add_field(name="📌 Version", value=server['latest_version'], inline=True)
            embed.add_field(name="📡 Latency", value=f"{str(server['latest_latency'])} ms", inline=True)
            embed.set_image(url="attachment://motd.png")
            await ctx.send(mention_msg, files=[favicon, motd], embed=embed)
        
    @track.error
    async def track_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor track ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336)
            await ctx.send(ctx.author.mention(), embed=embed)
        

def setup(bot):
    bot.add_cog(Track(bot))
