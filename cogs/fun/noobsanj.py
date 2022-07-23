import random
from discord.ext.commands import Cog, command
from discord.ext.commands import Bot
from discord import Embed
class NoobSanj(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['noobs', 'ns'])
    async def noobsanj(self, ctx):
        embed = Embed(title="Noob Sanj", description=f"Shoma {random.randint(1, 100)} noob hastid!", color=0x00D166)
        await ctx.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(NoobSanj(bot))
