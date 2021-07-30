from modules.config import Config

from discord import Embed
from discord.ext.commands import command, Cog

class Basics(Cog):
    """Basic commands cog

    All the basic 'INFO' , 'FAQ', etc commands of the tracker bot
    """
    
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["h"])
    async def help(self, ctx):
        """Simply sends help message 
        
        TODO:
            - Needs update
            - Receive help messages from config
        """
        embed = Embed(title="🥇・Live Stats category", description="Har 5 daghighe 3 server bartar ro ba tedad player ha neshoon mide", color=0x00D166)
        await ctx.send(embed=embed)

        embed = Embed(title="💎・All Players", description="Har 5 daghighe majmoo tedad player server haye irani ro neshoon mide", color=0x00D166)
        await ctx.send(embed=embed)

        embed = Embed(title="📈・Empty Count", description="Tedad server haei ke hich playeri nadaran ro neshoon mide", color=0x00D166)
        await ctx.send(embed=embed)

        embed = Embed(title="⏰・hourly-tracker", description="Har 1 saat chart tedad player server haye irani ro ersal mikone", color=0x00D166)
        await ctx.send(embed=embed)

    @command()
    async def add(self, ctx):
        """Simply sends 'how to add my server' message 
        
        TODO:
            - Making it ticket ish based instead of showing my id
        """
        embed = Embed(title="➕・add-your-server", description="Baraye ezafe kardan server khodetoon be @Alijk#2951 dm bedid", color=0x00D166)
        await ctx.send(embed=embed)
    

    @command()
    async def github(self, ctx):
        description = """You can find the project at [[IRMCTracker Github Repo]](https://github.com/Alijkaz/IRMCTracker)
        If you're a Python developer and you are interested in our project don't hesitate and start contributing the project :P"""
        embed = Embed(title="💻 Github [We're Open Source!]", description=description, color=0x3698cf)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member):
        """Adds default role to member and sends notification in admin channel

        TODO:
            - Send welcome message to user
        """
        embed = Embed(title=str(member) + ' summoned', color=0x00D166)
        await member.add_roles(member.guild.get_role(Config.Roles.DEFAULT))
        await self.bot.get_channel(Config.Channels.ADMIN).send(embed=embed)
        
    @Cog.listener()
    async def on_member_remove(self, member):
        """Sends a notification at member leave """
        embed = Embed(title=str(member) + ' did rm -rf /', color=0xA62019)
        await self.bot.get_channel(Config.Channels.ADMIN).send(embed=embed)

def setup(bot):
    bot.add_cog(Basics(bot))
