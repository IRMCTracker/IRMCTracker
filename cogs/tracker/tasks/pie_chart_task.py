import os

from modules.config import Config
from modules.tracker import get_servers_limit

from modules.utils import *

from nextcord.ext import tasks
from nextcord import Embed
from nextcord.ext.commands import Cog

import matplotlib.pyplot as plt


def draw_pie_chart():
    plt.rcParams['text.color'] = 'white'

    servers = get_servers_limit(8)

    names = [f"{server.name} [ {server.current_players} ]"  for server in servers]
    players = [server.current_players for server in servers]

    fig, ax = plt.subplots(figsize=(10,8))

    ax.pie(players, explode=(0.1, 0, 0, 0, 0, 0, 0, 0), labels=names, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax.axis('equal')

    output_file = random_cache_file('png')

    plt.savefig(output_file, transparent=True)

    plt.close(fig)

    return output_file

class PieChartTask(Cog):
    """Sending PIE Chart task
    """

    def __init__(self, bot):
        self.bot = bot

        # Running pie chart task
        self.pie_chart_task.start()

    @tasks.loop(minutes=1)
    async def pie_chart_task(self):
        await self.bot.wait_until_ready()

        chart_file = draw_pie_chart()

        embed = Embed(title="🥧 Pie Chart - Players of top Iranian servers", 
                        color=0x0099E1, timestamp=get_utc(),
                        url="https://mctracker.ir/server/list")
        embed.set_footer(text=f"Tracked by IRMCTracker", icon_url="https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128")

        cache_channel = self.bot.get_channel(Config.Channels.CACHE)

        file = await cache_channel.send(file=nextcord.File(chart_file))
        chart_url = file.attachments[0].url
        embed.set_image(url=chart_url)

        channel = self.bot.get_channel(Config.Channels.PIE)
        messages = await channel.history(limit=1).flatten()

        await messages[0].edit(content=None, embed=embed)

        os.remove(chart_file)


def setup(client):
    client.add_cog(PieChartTask(client))
