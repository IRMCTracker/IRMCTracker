import discord
from discord.ext import commands
from config import Config

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(ctx):
        await ctx.send("Pong!")

    @commands.command(aliases=["h"])
    async def help(self, ctx):
        embed = discord.Embed(title="🥇・Live Stats category", description="Har 5 daghighe 3 server bartar ro ba tedad player ha neshoon mide", color=0x00D166)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="💎・All Players", description="Har 5 daghighe majmoo tedad player server haye irani ro neshoon mide", color=0x00D166)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="📈・Empty Count", description="Tedad server haei ke hich playeri nadaran ro neshoon mide", color=0x00D166)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="⏰・hourly-tracker", description="Har 1 saat chart tedad player server haye irani ro ersal mikone", color=0x00D166)
        await ctx.send(embed=embed)

    @commands.command()
    async def add(self, ctx):
        embed = discord.Embed(title="➕・add-your-server", description="Baraye ezafe kardan server khodetoon be @Alijk#2951 dm bedid", color=0x00D166)
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_join(self, member):
        member.add_roles(self.bot.get_role(Config.Roles.DEFAULT))
        
def setup(bot):
    bot.add_cog(Basics(bot))
