from discord import Embed, File
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown
from modules.database import get_server_like
from modules.utils import *
import matplotlib as plt

from os import sep, remove
import uuid
from datetime import datetime

class ChartCommand(Cog):
    """Chart command

    Get server players chart of past week
    """

    def __init__(self, bot):
        self.bot = bot

    def draw_server_chart(self, server_id):
        url = "https://mctracker.ir/api/server/{}/records/daily/1".format(server_id)

        response = urlopen(url)

        results = json.loads(response.read())

        days = []
        players = []

        for day in results:
            days.append(to_persian(day))
            players.append(results[day][0]['players'])

        colors = []
        for player_count in players:
            if player_count >= 150:
                color = 'lime'
            elif 150 > player_count >= 100:
                color = 'darkgreen'
            elif 100 > player_count >= 80:
                color = 'mediumseagreen'
            elif 80 > player_count >= 60:
                color = 'orange'
            elif 60 > player_count >= 40:
                color = 'yellow'
            elif 40 > player_count >= 30:
                color = 'darkkhaki'
            elif 30 > player_count >= 20:
                color = 'orangered'
            elif 20 > player_count >= 10:
                color = 'firebrick'
            elif 10 > player_count:
                color = 'brown'

            colors.append(color)

        fig, ax = plt.subplots(figsize=(15,8))

        plt.title(f"MadCraft {to_persian('پلیر های یک هفته اخیر')} - {datetime.now():%Y-%m-%d %I:%M:%S}")
        plt.xlabel(to_persian('روز'), fontsize=10, labelpad=5)
        plt.ylabel(to_persian('تعداد پلیر'), fontsize=10, labelpad=5)
        
        ax.bar(days, players, color=colors)

        for index,data in enumerate(players):
            x = index - 0.11
            if len(str(data)) == 3:
                x = index - 0.2
            plt.text(x=x , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=12))

        output_file = "storage{}cache{}{}.png".format(sep, sep, uuid.uuid4())

        plt.savefig(output_file)

        return output_file

    @command(aliases=['charts'])
    @cooldown(6, 60, BucketType.user)
    async def chart(self, ctx, server=None):
        mention_msg = ctx.author.mention

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Dastoor vared shode motabar nist.", 
                                        description='Estefade dorost: ```.chart [servername]\nMesal: .chart madcraft```',
                                        color=0xF44336, timestamp=get_utc()))

        server = get_server_like(server)

        if server == None:
            return await ctx.send(mention_msg, embed=Embed(title=f"{self.bot.emoji('steve_think')} Server vared shode vojood nadarad!",
                                        description='Ba dastoor zir tamami server haro bebinid ```.servers```',
                                        color=0xF44336, timestamp=get_utc()))

        embed = Embed(title=f"👥 Player haye hafte akhir {server}", 
                        description=f"Liste balatarin meghdar player haye {server} dar hafte akhir", 
                        color=0x00D166, timestamp=get_utc())
        embed.set_footer(text=f"Tracked by IRMCTracker", icon_url="https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=128")

        output_file = self.draw_server_chart(server.id)

        file = File(output_file, filename="server_chart.png")
        embed.set_image(url="attachment://server_chart.png")

        await ctx.send(
            file=file, embed=embed
        )

        remove(output_file)
    
    @chart.error
    async def chart_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = Embed(title="Slow it Down!",
                    description=f"Shoma dar har daghighe faghat **6bar** emkan estefade az dastoor servers ro darid.\nBaraye estefade mojadad **{error.retry_after:.0f}** sanie sabr konid.",
                    color=0xF44336, timestamp=get_utc())
            await ctx.send(ctx.author.mention, embed=embed)

def setup(client):
    client.add_cog(ChartCommand(client))