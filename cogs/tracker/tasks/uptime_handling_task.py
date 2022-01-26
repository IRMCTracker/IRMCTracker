from time import time

from modules.config import Config
from modules.database import *
from modules.tracker import get_servers

from modules.utils import *

from nextcord.ext import tasks
from nextcord import File, Embed
from nextcord.ext.commands import Cog


class UptimeAlertsTask(Cog):
    """Alerting servers status
    """
    def __init__(self, bot):
        self.bot = bot
        
        # Running main bot tick
        self.uptime_alerts_task.start()

    @tasks.loop(minutes=1)
    async def uptime_alerts_task(self):
        await self.bot.wait_until_ready()

        """Refactored uptime registration system

        We have up_from field in database that changes to the timestamp that
        server starts to answer our requests so that we can calculate the time
        the server has been online
        Will set up_from field to a negative timestamp if server is offline in the latest check
        """
        alert_channel = self.bot.get_channel(Config.Channels.ALERTS)

        for server in get_servers():
            is_online = self.is_online(server)
            up_from_timestamp = server.up_from
            current_timestamp = round(time())

            embed = None
            
            # Means server is offline from last check in database
            if up_from_timestamp < 0:
                if is_online:
                    embed = Embed(
                        title=f"Server {server.name} online shod!",
                        description=f"\U0001f6a8 Server {server.name} lahazati pish online shod.\n\n⏰ Downtime: " + timestamp_ago(abs(server.up_from)),
                        color=0x00D166,
                        timestamp=get_utc()
                    )
                    server.up_from = current_timestamp

                # Logic of removing servers that were offline within past 30 days
                else:
                    # 30 days in seconds
                    expire_after_seconds = (60 * 60) * 24 * 30
                    # Convertin offline for seconds to offline for days
                    offline_days = (time() - abs(server.up_from))
                    
                    # Checking if server is offline for more than expire after seconds
                    if (offline_days > expire_after_seconds):
                        # Removing the server records
                        Records.delete().where(Records.server_id == server.id).execute()

                        # Removing the server metas
                        ServerMeta.delete().where(ServerMeta.server_id == server.id).execute()

                        # Now we gonna remove server
                        Server.delete().where(Server.id == server.id).execute()

                        # And we build up alert embed
                        embed = Embed(
                            title=f"💀 Server {server.name} hazf shod!",
                            description=f"Server {server.name} bedalil offline budan bishtar az 30 rooz az list tracking Tracker hazf shod.",
                            color=0xA62019,
                            timestamp=get_utc()
                        )

            # Means server is online from last check in database
            else:
                if not is_online:
                    embed = Embed(
                        title=f"❌ Server {server.name} offline shod!",
                        description=f"Server {server.name} lahazati pish az dastres kharej shod.\n\n⏰ Uptime: " + timestamp_ago(server.up_from),
                        color=0xff5757,
                        timestamp=get_utc()
                    )
                    server.up_from = -abs(current_timestamp)
            
            server.save()


            if embed != None:
                favicon = None
                if server.favicon_path:
                    favicon = File(server.favicon_path, filename="fav.png")
                    embed.set_thumbnail(url="attachment://fav.png")

                embed.set_footer(text=f"Tracked by IRMCTracker", icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=2048')

                await alert_channel.send(file=favicon,embed=embed)

    def is_online(self, server):
        if server.latest_latency == 0 and server.current_players == 0:
            return False
        return True        

def setup(client):
    client.add_cog(UptimeAlertsTask(client))
