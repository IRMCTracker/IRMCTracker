from cogs.tracker import Tracker
from discord.ext.commands.context import Context
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, NoEntryPointError

from discord.ext.commands import command, Cog, has_role, Bot as _bot
from modules.utils import get_logger


class Bot(Cog):
    """Low end bot management commands/events
    """

    def __init__(self, bot):
        self.bot: _bot = bot

    @Cog.listener()
    async def on_ready(self):
        get_logger().info(f"Booted and running on user: {self.bot.user}")

        try:
            tracker:Tracker = self.bot.get_cog('Tracker')
            await tracker.tracker_tick.start()
        except:
            get_logger().error('Failed to start Tracker#tracker_tick task')

    @command()
    @has_role('root')
    async def load(self, ctx: Context, *args: str):
        try:
            extension = args[0]
            if ".py" in extension:
                extension.replace(".py", "")
        except:
            ctx.send(":warning: Please provide an extension name")
        try:
            self.bot.load_extension(f'cogs.{extension}')
        except ExtensionNotFound:
            await ctx.send(f":warning: Extension **{extension}** doesn't exist!")
        except ExtensionAlreadyLoaded:
            await ctx.send(f":warning: Extension **{extension}** is already loaded!")
        except NoEntryPointError:
            await ctx.send(f":warning: Extension **{extension}** doesn't have a setup function")
        except ExtensionFailed as ex:
            await ctx.send(f":warning: Ran to a problem while running **{extension}**\n:x: Cause: **{ex}**")
        except Exception as ex:
            get_logger().info(
                f'unexpected error while loading an extension -- {ex}')
            ctx.send(
                f":interrobang: An unexpected problem occured!\n:x: Cause: **{ex}**\n:small_orange_diamond: You can issues here: https://github.com/Alijkaz/IRMCTracker/issues ")
        else:
            await ctx.send(f':white_check_mark: All done! Successfully loaded **{extension}**')

    @command()
    @has_role('root')
    async def unload(self, ctx: Context, *args: str):
        try:
            extension = args[0]
            if ".py" in extension:
                extension.replace(".py", "")
        except:
            ctx.send(":warning: Please provide an extension name")
        try:
            self.bot.unload_extension(f'cogs.{extension}')
        except ExtensionNotFound:
            await ctx.send(f":warning: Extension **{extension}** doesn't exist!")
        except ExtensionNotLoaded:
            await ctx.send(f":warning: Extension **{extension}** is not loaded yet to be unloaded!")
        except Exception as ex:
            get_logger().info(
                f'unexpected error while unloading an extension -- {ex}')
            ctx.send(
                f":interrobang: An unexpected problem occured!\n:x: Cause: **{ex}**\n:small_orange_diamond: You can issues here: https://github.com/Alijkaz/IRMCTracker/issues ")
        else:
            await ctx.send(f':white_check_mark: All done! Successfully unloaded **{extension}**')

    @command()
    @has_role('root')
    async def reload(self, ctx: Context, *args: str):
        try:
            extension = args[0]
            if ".py" in extension:
                extension.replace(".py", "")
        except:
            ctx.send(":warning: Please provide an extension name")
        try:
            self.bot.reload_extension(extension)
        except ExtensionNotFound:
            await ctx.send(f":warning: Extension **{extension}** doesn't exist!")
        except ExtensionNotLoaded:
            await ctx.send(f":warning: Extension **{extension}** is not loaded yet to be reloaded!")
        except NoEntryPointError:
            await ctx.send(f":warning: Extension **{extension}** doesn't have a setup function")
        except ExtensionFailed as ex:
            await ctx.send(f":warning: Ran to a problem while running **{extension}**\n:x: Cause: **{ex}**")
        except Exception as ex:
            get_logger().info(
                f'unexpected error while reloading an extension -- {ex}')
            ctx.send(
                f":interrobang: An unexpected problem occured!\n:x: Cause: **{ex}**\n:small_orange_diamond: You can issues here: https://github.com/Alijkaz/IRMCTracker/issues ")
        else:
            await ctx.send(f':white_check_mark: All done! Successfully reloaded **{extension}**')

    @command()
    @has_role('root')
    async def shutdown(self, ctx: Context):
        get_logger().info('Shutting down ...')
        bot: _bot = ctx.bot
        # await bot.logout() --> deprecated
        await bot.close()


def setup(bot: _bot):
    bot.add_cog(Bot(bot))
