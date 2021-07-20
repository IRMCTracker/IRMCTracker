import os
import discord
from discord.ext import commands
from discord.ext.commands import has_role
from config import Config


intents = discord.Intents().all()
bot = commands.Bot(command_prefix=Config.Bot.PREFIX, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('\nWe\'re up n running {0.user}'.format(bot))

    await bot.get_cog('Tracker').tracker_tick.start()

@bot.command()
@has_role('root')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f':white_check_mark: All done! Loaded **{extension}**')


@bot.command()
@has_role('root')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f':white_check_mark: All done! Unloaded **{extension}**')


@bot.command()
@has_role('root')
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f':white_check_mark: All done! Reloaded **{extension}**')

@bot.command()
@has_role('root')
async def shutdown(ctx):
    await ctx.bot.logout()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"\n- Loaded {filename}")


bot.run(Config.Bot.TOKEN)

