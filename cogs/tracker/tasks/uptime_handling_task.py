from time import time

from modules.config import Config
from modules.database import *
from modules.tracker import get_servers

from modules.utils import *

from discord.ext import tasks
from discord import File, Embed
from discord.ext.commands import Cog


class UptimeAlertsTask(Cog):
    """Alerting servers status
    """
    def __init__(self, bot):
        self.bot = bot
        
        # Running main bot tick
        self.alert_channel = None
        self.uptime_alerts_task.start()

    @tasks.loop(minutes=2)
    async def uptime_alerts_task(self):
        await self.bot.wait_until_ready()

        """Refactored uptime registration system

        We have up_from field in database that changes to the timestamp that
        server starts to answer our requests so that we can calculate the time
        the server has been online
        Will set up_from field to a negative timestamp if server is offline in the latest check
        """
        if (self.alert_channel == None):
            self.alert_channel = self.bot.get_channel(Config.Channels.ALERTS)

        for server in get_servers():
            server_is_online = is_online(server)
            up_from_timestamp = int(server.up_from)
            current_timestamp = round(time())

            embed = None
            
            # Means server is offline from last check in database
            if up_from_timestamp < 0:
                if server_is_online:
                    embed = Embed(
                        title=f"🟢 Server {server.name} online shod!",
                        description=f"\U0001f6a8 Server {server.name} lahazati pish online shod.\n\n⏰ Downtime: " + timestamp_ago(abs(server.up_from)),
                        color=0x00D166,
                        timestamp=get_utc()
                    )
                    server.up_from = current_timestamp
                    server.save()

                # Logic of removing servers that were offline within past 30 days
                else:
                    # 30 days in seconds
                    expire_after_seconds = (60 * 60) * 24 * 30
                    # Converting offline for seconds to offline for days
                    offline_days = (time() - abs(server.up_from))
                    
                    # Checking if server is offline for more than expire after seconds
                    if offline_days > expire_after_seconds:
                        server.is_active = False
                        server.save()

                        # And we build up alert embed
                        embed = Embed(
                            title=f"💀 Server {server.name} gheire faal shod!",
                            description=f"Server {server.name} bedalil offline budan bishtar az 30 rooz az list tracking Tracker hazf shod.",
                            color=0xA62019,
                            timestamp=get_utc()
                        )

            # Means server is online from last check in database
            else:
                if not server_is_online:
                    embed = Embed(
                        title=f"🔴 Server {server.name} offline shod!",
                        description=f"Server {server.name} lahazati pish az dastres kharej shod.\n\n⏰ Uptime: " + timestamp_ago(server.up_from),
                        color=0xff5757,
                        timestamp=get_utc()
                    )
                    server.up_from = -abs(current_timestamp)
                    server.save()

            if embed is not None:
                current_timestamp = str(int(time()))
                favicon = "https://mctracker.ir/api/servers/{}/favicon?v={}".format(server.id, current_timestamp)

                embed.set_footer(text=f"Tracked by IRMCTracker", icon_url='https://mctracker.ir/img/logo.png')

                await self.alert_channel.send(file=favicon,embed=embed)

def setup(client):
    client.add_cog(UptimeAlertsTask(client))
