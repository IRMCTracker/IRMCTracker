from config import get
from mcserver import MCTracker
from discord.ext import commands, tasks

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=3)
    async def tracker_tick(self):
        tracker = MCTracker()
        tracker.fetch_all()
        sorted_servers = tracker.sort_all()

        top1vc = self.bot.get_channel(866289711050784788)
        top2vc = self.bot.get_channel(866289915783544832)
        top3vc = self.bot.get_channel(866290014274584606)

        await top1vc.edit(name=f"🥇 {sorted_servers[0].get_name()} [{sorted_servers[0].get_online_players()}]")
        await top2vc.edit(name=f"🥈 {sorted_servers[1].get_name()} [{sorted_servers[1].get_online_players()}]")
        await top3vc.edit(name=f"🥉 {sorted_servers[2].get_name()} [{sorted_servers[2].get_online_players()}]")

def setup(client):
    client.add_cog(Tracker(client))
