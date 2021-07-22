from discord import Embed
from discord.ext.commands import command, Cog

from modules.tracker import MCServer
from modules.database import get_servers_like


class Track(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(aliases=['status','stats'])
    async def track(self, ctx, server=None):
        if server == None:
            return await ctx.send(embed=Embed(title='Dastoor vared shode motabar nist.', 
                                        description='Estefade dorost: ```-track [servername] | Ex. -track madcraft```',
                                        color=0xF44336))
        
        servers_alike = get_servers_like(server)

        if len(servers_alike == 0):
            return await ctx.send(embed=Embed(title='Server vared shode vojood nadarad!',
                                        description='ba dastoor ```-servers``` tamami server haro bebinid!'))
        elif len(servers_alike > 1):
            alike_names = []
            [alike_names.append(server['name']) for server in servers_alike]

            return await ctx.send(embed=Embed(title='Server morede nazar peida nashod!',
                                        description='Shayad manzooretoon yeki az in hast: **' + ' | '.join(alike_names) + '**'))
        elif len(servers_alike) == 1:
            embed=Embed(title="", color=0x1bd027)
            embed.set_author(name='💎 MadCraft')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/476394314776313876/867524069863587890/download.png')
            embed.add_field(name="🌐 Address", value="Hub.MadCraft.IR", inline=False)
            embed.add_field(name="👥 Online Players", value="10", inline=True)
            embed.add_field(name="🥇 Top Players Record", value="26", inline=True)
            embed.add_field(name="🔗 Discord", value="https://discord.gg/bZWSScwQ7a", inline=False)
            embed.add_field(name="📌 Version", value="1.16 - 1.17", inline=True)
            embed.add_field(name="📡 Latency", value="8 ms", inline=True)
            embed.set_image(url='https://cdn.discordapp.com/attachments/476394314776313876/867528098822881290/unknown.png')
            await ctx.send(embed=embed)
        
            

def setup(bot):
    bot.add_cog(Track(bot))
