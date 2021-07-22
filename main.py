from modules.utils.logging import get_logger
import sys
from os import listdir

from discord import Intents
from discord.ext.commands import Bot

from modules.config import Env
from modules.database import create_tables
from modules.tracker import MCTracker

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        sys.exit("You have not entered any args.\nAvailable args: [run , test, db]")

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
    
    elif ':' in args[0]:
        cmd , child = args[0].split(':')

        if cmd == 'db':
            if child == 'update':
                tracker = MCTracker()
                tracker.fetch_and_sort()
                tracker.update_servers_database_meta()
            else:
                get_logger().error('Wrong command child! Use [ update ]')

