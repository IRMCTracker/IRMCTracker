import sys
import asyncio
import os

from discord import Intents
from discord.ext.commands import Bot

from modules.config import Env
from modules.utils import get_logger
from modules.tracker import MCTracker
from modules.database import create_tables, database

from threading import Thread


def run_discord_bot():
    """ Running discord bot

    Notes:
        - help_command is None so that we can introduce the command later
        - Having intents.all() makes it possible to do mass actions with members
        - Will load every single cog in ~/cogs/ directory and run the bot    
    """ 
    
    bot = Bot(command_prefix=Env.PREFIX,
              intents=Intents().all(), help_command=None)
    bot.tempdata = {}

    loaded_extensions = {}

    """Loading all the py files below 'cogs/*' as extensions
    """
    for path, subdirs, files in os.walk('cogs/'):
        for name in files:
            if name.endswith('.py'):
                filename = os.path.join(path, name).replace('/', '.').replace('\\', '.')[:-3]
                cog_name = name[:-3].split('.')[-1]
                
                loaded_extensions[cog_name] = filename

                bot.load_extension(filename)

                print(f"\n- Loaded {filename}")

    bot.loaded_extensions = loaded_extensions

    bot.run(Env.TOKEN)

    return bot


if __name__ == "__main__":
    args = sys.argv[1:]
    db = database.connect()

    if len(args) == 0:
        sys.exit(
            "You have not entered any args.\nAvailable args: [run , test, db]")

    if args[0] == 'run':
        # Creating the database tables (and the actual database file if doesnt exist)
        create_tables()

        if not Env.DEBUG:
            # Running the database update task in another thread so that it doesnt interfere with the actual bot
            thread = Thread(target = MCTracker().update_task, daemon=True).start()

        bot = run_discord_bot()

        bot.db = db

    elif args[0] == 'test':
        from tests.test_basic import *

    elif ':' in args[0]:
        cmd, child = args[0].split(':')

        if cmd == 'db':
            if child == 'update':
                tracker = MCTracker()
                tracker.fetch_and_sort()
                tracker.update_servers_in_database()

            else:
                get_logger().error('Wrong command child! Use [ update ]')
