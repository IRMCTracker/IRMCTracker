from modules.config import Config
from modules.tracker import all_players_count, zero_player_servers_count, get_servers_by_record
from modules.database.models.records import get_highest_players

from modules.utils import *

from discord.ext import tasks
from discord import Embed
from discord.ext.commands import Cog


class StatsChannelsTask(Cog):
    """Updating statistics channels task
    """

    def __init__(self, bot):
        self.bot = bot

        # Running stats channels update task
        self.stats_channels_task.start()

    @tasks.loop(minutes=1)
    async def stats_channels_task(self):
        """Updating stats voice channels
        """
        get_logger().info("Updating stats channels")

        await self.bot.wait_until_ready()

        await self.bot.get_channel(Config.Channels.ALL).edit(
            name=f"💎・All「{all_players_count()}👥」"
        )
        await self.bot.get_channel(Config.Channels.EMPTY).edit(
            name=f"📈・Empty「{zero_player_servers_count()}🔨」"
        )  

        await self.update_records_text()
    
    async def update_records_text(self):
        channel = self.bot.get_channel(Config.Channels.RECORD)
        messages = await channel.history(limit=1).flatten()

        embed = Embed(title="💎 Top Records | رکورد سرور های ایرانی",
                        description="لیست بالا ترین رکورد سرور های ایرانی بر اساس تعداد پلیر",
                        color=0x4CAF50, timestamp=get_utc())

        i = 0
        for server in get_servers_by_record():
            # To prevent discord fields limit
            if i > 24: break
            
            prefix = get_medal_emoji(i)

            embed.add_field(
                name=f"{prefix} • {str(server.name).capitalize()}", 
                value=f"「 {get_highest_players(server)}👥 Players 」", 
                inline=False
            )

            i += 1

        embed.set_footer(text=f"Tracked by IRMCTracker")
        embed.set_image(url="https://mctracker.ir/img/motd.png")

        await messages[0].edit(content=None, embed=embed)

def setup(client):
    client.add_cog(StatsChannelsTask(client))
