from os.path import exists

from discord import Embed, File
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown
from modules.tracker import get_servers
from modules.database import get_server_like, get_highest_players
from modules.database.models.server_meta import get as get_meta
from modules.utils import *

class TrackerGlobal(Cog):
    """Track command

    To get information of a specific server

    TODO:
        - Add a command for fetching custom domain/ip addresses
    """

    @command(aliases=['status','stats', 'server'])
    @cooldown(6, 60, BucketType.user)
    async def track(self, ctx, server=None):
        """Track command for getting information about servers
        """

        mention_msg = ctx.author.mention

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Dastoor vared shode motabar nist.", 
                                        description='Estefade dorost: ```.track [servername]\nMesal: .track madcraft```',
                                        color=0xF44336, timestamp=get_utc()))

        server = get_server_like(server)

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Server vared shode vojood nadarad!",
                                        description='Ba dastoor zir tamami server haro bebinid ```.servers```',
                                        color=0xF44336, timestamp=get_utc()))
        else:
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

            uptime = timestamp_ago(server.up_from)

            if server.latest_latency == 0:
                embed = Embed(title=f"🔴 {server.name}", 
                                description=f"Server morede nazar shoma dar hale hazer offline hast : (\n\n⏰ Downtime: {timestamp_ago(abs(server.up_from))}", 
                                color=0xc62828, 
                                timestamp=get_utc())
                return await ctx.send(mention_msg, embed=embed)
            if server.motd_path == 'null' or not exists(server.motd_path):
                server.motd_path = 'storage/static/banner.png'
            
            embed=Embed(title=f"💎 {server.name}", 
                            description=f"{server.description if server.description != None else ' '}", 
                            color=0x1bd027, 
                            url = "https://mctracker.ir/server/{}".format(str(server.id)),
                            timestamp=get_utc())

            embed.set_footer(
                text=f"Tracked By IRMCTracker",
                icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128'
            )

            favicon = File(server.favicon_path, filename="image.png")

            if server.motd_path == None:
                server.motd_path = 'storage/static/banner.png'
                            
            motd = File(server.motd_path, filename="motd.png")
            embed.set_thumbnail(url="attachment://image.png")

            ip = ""
            if server.ip != None:
                ip = f"( **{server.ip}** )"

            embed.add_field(name="「🌐」 Address ►", value=f"{capitalize_address(server.address)} {ip}", inline=False)
            embed.add_field(name="「👥」 Online Players ►", value="{} **/** {}".format(str(server.current_players), str(server.max_players)), inline=True)
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
                
            if server.channel_id != 0:
                server_channel = self.bot.get_channel(server.channel_id).mention
                embed.add_field(
                    name="「📢」 Channel ►",
                    value=server_channel,
                    inline=False
                )

            socials_message = '\n'.join(socials)
            if len(socials) == 0:
                socials_message = 'No Socials Set'

            embed.add_field(
                name=f"「{self.bot.emoji('people')}」 Socials ►", 
                value=socials_message, 
                inline=False
            )



            embed.set_image(url="attachment://motd.png")
            await ctx.send(mention_msg, files=[favicon, motd], embed=embed)
        
    @track.error
    async def track_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor track ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336, timestamp=get_utc())
            await ctx.send(ctx.author.mention, embed=embed)
        

def setup(bot):
    bot.add_cog(TrackerGlobal(bot))
