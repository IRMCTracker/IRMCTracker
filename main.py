import os
import discord
from discord.ext import commands
from config import Config, get


intents = discord.Intents().all()
bot = commands.Bot(command_prefix=Config.Bot.PREFIX, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('\nWe\'re up n running {0.user}'.format(bot))

    # tracker_cog = bot.get_cog('Tracker')
    # await tracker_cog.tracker_tick.start()

@bot.command()
async def load(ctx, extension):
    if ctx.author.id == 296565827115941889:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f':white_check_mark: All done! Loaded **{extension}**')


@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == 296565827115941889:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f':white_check_mark: All done! Unloaded **{extension}**')


@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == 296565827115941889:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f':white_check_mark: All done! Reloaded **{extension}**')

@bot.command()
async def shutdown(ctx):
    if ctx.author.id == 296565827115941889:
        await ctx.bot.logout()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"\n- Loaded {filename}")


bot.run(Config.Bot.TOKEN)

