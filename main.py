from modules.utils.logging import get_logger
import sys
from os import listdir

from time import sleep

from discord import Intents
from discord.ext.commands import Bot

from modules.config import Env
from modules.database import create_tables
from modules.tracker import MCTracker

import asyncio
from threading import Thread


def update_servers_tick():
    asyncio.set_event_loop(asyncio.new_event_loop())
    while True:
        tracker = MCTracker()
        tracker.fetch_and_sort()

        tracker.update_servers_motd()

        sleep(50)
        
def run_discord_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())

    bot = Bot(command_prefix=Env.PREFIX, intents=Intents().all(), help_command=None)

    for filename in listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"\n- Loaded {filename}")

    bot.run(Env.TOKEN)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        sys.exit("You have not entered any args.\nAvailable args: [run , test, db]")

    if args[0] == 'run':
        create_tables()

        Thread(target=update_servers_tick, daemon=True).start()
        Thread(target=run_discord_bot, daemon=True).start()


    elif args[0] == 'test':
        from tests.test_basic import *
    
    elif ':' in args[0]:
        cmd , child = args[0].split(':')

        if cmd == 'db':
            if child == 'update':
                tracker = MCTracker()
                tracker.fetch_and_sort()
                tracker.update_servers_in_database()

            else:
                get_logger().error('Wrong command child! Use [ update ]')
