from discord.ext import Cog, command


class Skin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def skin(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Skin(bot))
