from discord import Embed
from discord.ext.commands import Cog, command, has_role

from modules.database import update_server, insert_server, remove_server, server_meta, get_server
from modules.tracker import MCTracker
from modules.utils import get_beautified_dt

class Admin(Cog):
    """Tracker Admin commands
    
    All the admin commands that will manage and do operations within the tracker bot
    """
    
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["newserver"])
    @has_role('root')
    async def addserver(self, ctx, name, address):
        insert_server(name, address)
        await ctx.send(f"Server **{name}** with address **{address}** added to database")

    @command(aliases=["rmserver"])
    @has_role('root')
    async def removeserver(self, ctx, name):
        remove_server(name)
        await ctx.send(f"Removed server **{name}**")


    @command(aliases=["updatediscord"])
    @has_role('root')
    async def setsocial(self, ctx, social: str, server_name: str, value: str):
        socials = ['telegram', 'website', 'instagram', 'shop', 'discord']

        if social in socials:
            server = get_server(server_name)
            if server == None:
                return await ctx.send('Server vared shode motabar nist')

            server_meta.add(server, social, value)
            await ctx.send(f"Server **{server_name}** {social} set shod be {value}")
        else:
            await ctx.send('Social vared shode nadorost ast.')

    @command(aliases=["settopplayer"])
    @has_role('root')
    async def settopplayers(self, ctx, name, top_players):
        update_server(name, top_players=top_players)
        await ctx.send(f"Server **{name}** top players set to {top_players}")

    @command(aliases=["updateaddress"])
    @has_role('root')
    async def setaddress(self, ctx, name, address):
        update_server(name, address=address)
        await ctx.send(f"Server **{name}** address set to **{address}**")


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
        embed.set_footer(text=f"{ctx.author.name} - {get_beautified_dt()}", icon_url='https://cdn.discordapp.com/avatars/296565827115941889/e7173c0bae58262ea565f746cecd6b8b.webp?size=128')
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


    @command(has_role='root')
    @has_role('root')
    async def sendhourly(self,ctx):
        await self.bot.get_cog('TrackerTasks').send_chart()

    @command(has_role='root')
    @has_role('root')
    async def updatedb(self,ctx):
        MCTracker().update_servers_database()

    @command()
    @has_role('root')
    async def updatechannels(self,ctx):
        await self.bot.get_cog('TrackerTasks').update_channels()

    @command()
    @has_role('root')
    async def updatetoptext(self,ctx):
        await self.bot.get_cog('TrackerTasks').update_top_text()

    @command()
    @has_role('root')
    async def updaterecordstext(self,ctx):
        await self.bot.get_cog('TrackerTasks').update_records_text()

    @command(pass_context = True)
    @has_role('root')
    async def clear(self, ctx, number: int):
        mgs = []
        async for x in self.bot.logs_from(ctx.message.channel, limit = number):
            mgs.append(x)
        await self.bot.delete_messages(mgs)

def setup(bot):
    bot.add_cog(Admin(bot))
