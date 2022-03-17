from modules.config import Config
from modules.database.models.records import get_all_records_count
from modules.database.models.vote import get_all_votes_count
from modules.tracker import get_servers

from modules.utils import *

from nextcord.ext import tasks
from nextcord.ext.commands import Cog


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

        self.MEMBERS_CHANNEL = self.bot.get_channel(Config.Channels.MEMBERS)
        self.SERVERS_CHANNEL = self.bot.get_channel(Config.Channels.SERVERS)
        self.VOTES_CHANNEL = self.bot.get_channel(Config.Channels.VOTES)
        self.TRACKS_CHANNEL = self.bot.get_channel(Config.Channels.TRACKS)

        await self.update_members_count()
        await self.update_servers_count()
        await self.update_votes_count()
        await self.update_tracks_count()

    async def update_members_count(self):

        guild = self.bot.get_guild(Config.GUILD_ID)
        await self.MEMBERS_CHANNEL.edit(
            name=f"👥・ Members「{humanize_number(guild.member_count)}」"
        )

    async def update_servers_count(self):
        servers_count = str(len(get_servers()))
        await self.SERVERS_CHANNEL.edit(
            name=f"💻・ Servers「{humanize_number(servers_count)}」"
        )

    async def update_votes_count(self):
        await self.VOTES_CHANNEL.edit(
            name=f"😄・ Votes「{humanize_number(get_all_votes_count())}」"
        )

    async def update_tracks_count(self):
        await self.TRACKS_CHANNEL.edit(
            name=f"🔗・ Tracks「{humanize_number(get_all_records_count())}」"
        )

def setup(client):
    client.add_cog(StatsTask(client))
