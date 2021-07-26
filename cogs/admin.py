from discord import Embed
from discord.ext.commands import Cog, command, has_role

from modules.database import update_server
from modules.utils import get_beautified_dt

class Admin(Cog):
    """Tracker Admin commands
    
    All the admin commands that will manage and do operations within the tracker bot
    """
    
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["updatediscord"])
    async def setdiscord(self, ctx, name, discord):
        """Changing the default(null) discord of a server in database
        
        TODO:
            - Will produce error if the desired server doesnt exist
            - Need to move all admin commands to this cog
        """
        update_server(name, discord=discord)
        await ctx.send(f"Server **{name}** discord set to {discord}")

    @command()
    @has_role('root')
    async def update(self, ctx, *, update: str):
        """Sends update message to chanelog channel

        TODO:
            - Get chanelog channel id, picture, icon from config or db
        """

        # Making '-' bold in the message
        update = update.replace('-', '**-**')
        channel = self.bot.get_channel(868223162796625920)
        embed = Embed(title=f"🎈 Chanelog", description=update, color=0x536dfe)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/866594343551500308/868231230729125968/chanelog.png')
        embed.set_footer(text=f"{ctx.author.name} - {get_beautified_dt()}", icon_url='https://cdn.discordapp.com/avatars/296565827115941889/f6c762a29a13c63b1d16e4b970a80c17.webp?size=128')
        await channel.send(embed=embed)

    @command()
    @has_role('root')
    async def guidelines(self, ctx):
        """Sends guideline message to guidelines channel

        TODO:
            - Get guidelines message, channel id, picture, icon from config or db
        """
        
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
    bot.add_cog(Admin(bot))
