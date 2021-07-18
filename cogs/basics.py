import discord
from discord.ext import commands


class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(ctx):
        await ctx.send("Pong!")

def setup(bot):
    bot.add_cog(Basics(bot))
