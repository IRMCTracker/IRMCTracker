import sys
import os

from discord import Intents
from discord.ext.commands import Bot

from modules.config.config_values import Config
from modules.utils import get_logger
from modules.database import create_tables, database

def run_discord_bot():
    """ Running discord bot

    Notes:
        - help_command is None so that we can introduce the command later
        - Having intents.all() makes it possible to do mass actions with members
        - Will load every single cog in ~/cogs/ directory and run the bot    
    """ 
    
    bot = Bot(command_prefix=Config.Bot.PREFIX,
              intents=Intents().all(), help_command=None, case_insensitive=True)
    
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

                get_logger().info(f"Loaded {filename}")

    bot.loaded_extensions = loaded_extensions

    bot.run(Config.Bot.TOKEN)

    return bot


if __name__ == "__main__":
    args = sys.argv[1:]
    db = database.connect()

    if len(args) == 0:
        sys.exit(
            "You have not entered any args.\nAvailable args: [run, run:bot, run:tracker , db]")

    if args[0] == 'run':
        # Creating the database tables (and the actual database file if doesnt exist)
        create_tables()

        bot = run_discord_bot()

        bot.db = db