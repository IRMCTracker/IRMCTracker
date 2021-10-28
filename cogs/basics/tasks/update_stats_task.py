from modules.config import Config
from modules.database.models.records import get_all_records_count
from modules.database.models.vote import get_all_votes_count
from modules.tracker import get_servers

from modules.utils import *

from discord.ext import tasks
from discord.ext.commands import Cog


class StatsTask(Cog):
    """Updating tracker stats channels task
    """

    def __init__(self, bot):
        self.bot = bot

        # Running stats updating task
        self.stats_task.start()

    @tasks.loop(minutes=5)
    async def stats_task(self):
        await self.bot.wait_until_ready()

        await self.update_members_count()
        await self.update_servers_count()
        await self.update_votes_count()
        await self.update_tracks_count()

    async def update_members_count(self):
        channel = self.bot.get_channel(Config.Channels.MEMBERS)
        guild = self.bot.get_guild(Config.GUILD_ID)
        await channel.edit(
            name=f"👥・ Members「{humanize_number(guild.member_count)}」"
        )

    async def update_servers_count(self):
        channel = self.bot.get_channel(Config.Channels.SERVERS)
        servers_count = str(len(get_servers()))
        await channel.edit(
            name=f"💻・ Servers「{humanize_number(servers_count)}」"
        )

    async def update_votes_count(self):
        channel = self.bot.get_channel(Config.Channels.VOTES)
        await channel.edit(
            name=f"😄・ Votes「{humanize_number(get_all_votes_count())}」"
        )

    async def update_tracks_count(self):
        channel = self.bot.get_channel(Config.Channels.TRACKS)
        await channel.edit(
            name=f"🔗・ Tracks「{humanize_number(get_all_records_count())}」"
        )

def setup(client):
    client.add_cog(StatsTask(client))
