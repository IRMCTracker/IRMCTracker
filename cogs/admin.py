import discord
from discord.ext import commands

from modules.database import update_server

class Admin(commands.Cog):
    """Tracker Admin commands
    
    All the admin commands that will manage and do operations within the tracker bot
    """
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["updatediscord"])
    async def setdiscord(self, ctx, name, discord):
        """Changing the default(null) discord of a server in database
        
        TODO Will produce error if the desired server doesnt exist
        """
        update_server(name, discord=discord)
        await ctx.send(f"Server **{name}** discord set to {discord}")

def setup(bot):
    bot.add_cog(Admin(bot))
