from modules.tracker import MCTracker, get_servers, all_players_count

from modules.utils import *

from discord.ext import tasks
from discord.ext.commands import Cog

import time

class VoteRenewTask(Cog):
    """Renewing vote task
    We do that because discord interactions won't last longer than an hour
    So we'll be renewing the interaction(servers vote menu) every 50min
    """

    def __init__(self, bot):
        self.bot = bot

        # Running vote renew task
        self.vote_renew.start()

    @tasks.loop(minutes=40)
    async def vote_renew(self):
        await self.bot.wait_until_ready()

        if self.bot.vote_message_id != 0:
            channel = self.bot.get_channel(self.bot.vote_channel_id)
            old_message = await channel.fetch_message(self.bot.vote_message_id)
            await channel.delete_messages([old_message])
            await self.bot.get_cog("Vote").send_vote_message(channel)


def setup(client):
    client.add_cog(VoteRenewTask(client))
