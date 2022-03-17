from nextcord import Activity, ActivityType
from nextcord.ext import tasks
from nextcord.ext.commands import Cog

from modules.tracker import get_servers, all_players_count


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

        if self.counter == 0:
            status_text = f"👥 {all_players_count()} Players"
            self.counter = 1
        else:
            status_text = f"💻 {str(len(get_servers()))} Servers"
            self.counter = 0

        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=status_text
            )
        )
    
def setup(client):
    client.add_cog(ActivityTask(client))
