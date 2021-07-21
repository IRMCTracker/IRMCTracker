import sys
from os import listdir

from discord import Intents
from discord.ext.commands import Bot

from modules.config import Config, Env
from modules.database import create_tables

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        sys.exit("You have not entered any args.\nAvailable args: [run , test]")

    if args[0] == 'run':
        create_tables()

        bot = Bot(command_prefix=Env.PREFIX, intents=Intents().all(), help_command=None)

        for filename in listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"\n- Loaded {filename}")

        bot.run(Env.TOKEN)
    elif args[0] == 'test':
        from tests.test_basic import *

