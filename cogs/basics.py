from modules.config import Config
from modules.utils import get_beautified_dt

from discord import Embed
from discord.ext.commands import command, Cog, has_role

class Basics(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["h"])
    async def help(self, ctx):
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
        embed = Embed(title="➕・add-your-server", description="Baraye ezafe kardan server khodetoon be @Alijk#2951 dm bedid", color=0x00D166)
        await ctx.send(embed=embed)
        
    @Cog.listener()
    async def on_member_join(self, member):
        embed = Embed(title=str(member) + ' summoned', color=0x00D166)
        await member.add_roles(member.guild.get_role(Config.Roles.DEFAULT))
        await self.bot.get_channel(Config.Channels.ADMIN).send(embed=embed)
        
    @Cog.listener()
    async def on_member_remove(self, member):
        embed = Embed(title=str(member) + ' did rm -rf /', color=0xA62019)
        await self.bot.get_channel(Config.Channels.ADMIN).send(embed=embed)

    @command()
    @has_role('root')
    async def update(self, ctx, *, update: str):
        update = update.replace('-', '**-**')
        channel = self.bot.get_channel(868223162796625920)
        embed = Embed(title=f"🎈 Chanelog", description=update, color=0x536dfe)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/866594343551500308/868231230729125968/chanelog.png')
        embed.set_footer(text=f"Alijk - {get_beautified_dt()}", icon_url='https://cdn.discordapp.com/avatars/296565827115941889/f6c762a29a13c63b1d16e4b970a80c17.webp?size=128')
        await channel.send(embed=embed)

    @command()
    @has_role('root')
    async def guidelines(self, ctx):
        description = """
        Our guidelines are simple and easy to follow but we're open to any suggestions for our guidelines

        **» Chatting Rules**
        **-**   Please be respectful to everyone
        **-**   Swearing or flooding is not allowed
        **-**   Advertising in channels that we don't specifically allow is forbidden
        **-**   Please do not harass, bully, talk about pornographic, pedophilia and etc

        **» Additional Rules**
        **-**   Please do not DM advertise, we're doing all we can to let you guys advertise your servers
        **-**   Obey discord T.O.S

        **Links:**
        » Discord:  https://discord.gg/ey3FmsMfmp
        """
        channel = self.bot.get_channel(867121964229066752)
        embed = Embed(title=f"📌 Guidelines", description=description, color=0x43a047)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/866594343551500308/868239327715549184/guidelines.png')
        embed.set_footer(text=f"IRMCTracker", icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=2048')
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Basics(bot))
