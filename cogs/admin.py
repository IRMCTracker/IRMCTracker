import discord
from discord.ext import commands

from modules.database import update_server

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["updatediscord"])
    async def setdiscord(self, ctx, name, discord):
        await ctx.send(name)
        update_server(name, discord=discord)
        await ctx.send(f"Server **{name}** discord set to {discord}")

def setup(bot):
    bot.add_cog(Admin(bot))
