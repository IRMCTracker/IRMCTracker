import discord
from discord.ext import commands
from discord.ext.commands import has_role


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener
    async def on_ready(self):
        print('\nWe\'re up n running {0.user}'.format(bot))

        await self.bot.get_cog('Tracker').tracker_tick.start()

    @commands.command()
    @has_role('root')
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f':white_check_mark: All done! Loaded **{extension}**')


    @commands.command()
    @has_role('root')
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f':white_check_mark: All done! Unloaded **{extension}**')


    @commands.command()
    @has_role('root')
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f':white_check_mark: All done! Reloaded **{extension}**')

    @commands.command()
    @has_role('root')
    async def shutdown(self, ctx):
        await ctx.bot.logout()

def setup(bot):
    bot.add_cog(Bot(bot))

