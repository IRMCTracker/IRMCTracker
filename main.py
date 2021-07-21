import os
from discord import Intents
from discord.ext.commands import Bot
from modules.config import Config

if __name__ == "__main__":
    bot = Bot(command_prefix=Config.Bot.PREFIX, intents=Intents().all(), help_command=None)

    [bot.load_extension(f'cogs.{filename[:-3]}') for filename in os.listdir('./cogs') ]

bot.run(Config.Bot.TOKEN)

