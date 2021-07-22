from discord import Embed, File
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown

from modules.tracker import MCServer
from modules.database import get_servers_like


class Track(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(aliases=['status','stats'])
    @cooldown(2, 60, BucketType.user)
    async def track(self, ctx, server=None):
        if server == None:
            return await ctx.send(embed=Embed(title='Dastoor vared shode motabar nist.', 
                                        description='Estefade dorost: ```-track [servername]\nMesal: -track madcraft```',
                                        color=0xF44336))
        
        servers_alike = get_servers_like(server)

        if len(servers_alike) == 0:
            return await ctx.send(embed=Embed(title='Server vared shode vojood nadarad!',
                                        description='Ba dastoor zir tamami server haro bebinid ```-servers```',
                                        color=0xF44336))
        elif len(servers_alike) > 1:
            alike_names = []
            [alike_names.append(server['name']) for server in servers_alike]

            return await ctx.send(embed=Embed(title='Server morede nazar peida nashod!',
                                        description='Shayad manzooretoon yeki az in hast: **' + ' | '.join(alike_names) + '**',
                                        color=0x689F38))
        elif len(servers_alike) == 1:
            server = servers_alike[0]
            discord = server['discord'] if server['discord'] != 'null' else 'Not Set'


            embed=Embed(title="", color=0x1bd027)
            embed.set_author(name=f"💎 {server['name']}")

            file = File(server['favicon'], filename="image.png")
            embed.set_thumbnail(url="attachment://image.png")

            embed.add_field(name="🌐 Address", value=server['address'], inline=False)
            embed.add_field(name="👥 Online Players", value=server['current_players'], inline=True)
            embed.add_field(name="🥇 Top Players Record", value=server['top_players'], inline=True)
            embed.add_field(name="🔗 Discord", value=discord, inline=False)
            embed.add_field(name="📌 Version", value=server['latest_version'], inline=True)
            embed.add_field(name="📡 Latency", value=server['latest_latency'], inline=True)
            # embed.set_image(url='https://cdn.discordapp.com/attachments/476394314776313876/867528098822881290/unknown.png')
            await ctx.send(file=file, embed=embed)
        
    @track.error
    async def track_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **2bar** emkan estefade az dastoor track ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336)
            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Track(bot))
