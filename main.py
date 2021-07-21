from os import listdir
from discord import Intents
from discord.ext.commands import Bot
from modules.config import Config

if __name__ == "__main__":
    bot = Bot(command_prefix=Config.Bot.PREFIX, intents=Intents().all(), help_command=None)

    for filename in listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"\n- Loaded {filename}")

bot.run(Config.Bot.TOKEN)

