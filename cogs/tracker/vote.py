from nextcord import Embed
from nextcord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown
from modules.config import Config
from modules.database import get_server_like
from modules.utils import *

class VoteCommand(Cog):
    """Vote command cog

    Shows the URL to vote the server
    """

    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['v'])
    @cooldown(6, 60, BucketType.user)
    async def vote(self, ctx, server=None):
        """Sending vote URL of the specific server
        """

        if ctx.channel.id != Config.Channels.TRACK_USAGE_CHANNEL:
            await ctx.message.add_reaction('❌')
            return

        mention_msg = ctx.author.mention

        if server is None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Dastoor vared shode motabar nist.", 
                                        description='Estefade dorost: ```.vote [servername]\nMesal: .vote madcraft```',
                                        color=0xF44336, timestamp=get_utc()))

        server = get_server_like(server)

        if server is None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Server vared shode vojood nadarad!",
                                        description='Ba dastoor zir tamami server haro bebinid ```.servers```',
                                        color=0xF44336, timestamp=get_utc()))
        else:
            vote_url = f"https://mctracker.ir/server/{server.id}/vote"
            description = f"""Agar {server.name} ro doost darid mitoonid ba vote dadan az [INJA]({vote_url}) azashoon hemayat konid!
            
            Ba vote dadan mitoonid az ghabeliat haei ke {server.name} baraye vote amade karde bahremand beshid!"""
            embed = Embed(title=f"✌ Vote {server.name}", description=description, color=0x4CAF50, timestamp=get_utc(), url=vote_url)
            embed.set_footer(
                text=f"Tracked By IRMCTracker",
                icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128'
            )
            await ctx.send(embed=embed)

    @vote.error
    async def track_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor track ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336, timestamp=get_utc())
            await ctx.send(ctx.author.mention, embed=embed)

def setup(client):
    client.add_cog(VoteCommand(client))
