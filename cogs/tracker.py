from discord.ext import commands, tasks

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def tracker_tick(self):
        channel = self.bot.get_channel(866288077239484496)
        await channel.send("test")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('hey!')

def setup(client):
    client.add_cog(Tracker(client))
