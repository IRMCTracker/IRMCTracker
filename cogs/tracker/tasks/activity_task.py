from modules.tracker import MCTracker, get_servers, all_players_count

from modules.utils import *

from nextcord.ext import tasks
from nextcord import Activity, ActivityType
from nextcord.ext.commands import Cog


class ActivityTask(Cog):
    """Updating activity task
    """

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

        # Running activity updating task
        self.activity_task.start()

    # TRACKER TASKS
    @tasks.loop(seconds=15)
    async def activity_task(self):
        await self.bot.wait_until_ready()

        players_count = all_players_count()
        servers_count = str(len(get_servers()))

        if self.counter % 2 == 0:
            status_text = f"👥 {players_count} Players"
        else:
            status_text = f"💻 {servers_count} Servers"

        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=status_text
            )
        )

        self.counter += 1

    
def setup(client):
    client.add_cog(ActivityTask(client))
