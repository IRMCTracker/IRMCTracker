import os
from datetime import datetime as dt
from modules.config import Config
from modules.tracker import MCTracker, get_servers, all_players_count, zero_player_servers_count
from modules.utils import shortified, get_beautified_dt

from discord.ext import tasks
from discord import File, Embed, Activity, ActivityType
from discord.ext.commands import Cog

class Tracker(Cog):
    """Doing all the automated tracking->discord tasks

    """

    def __init__(self, bot):
        self.bot = bot
        self.servers = get_servers()
    
    @tasks.loop(minutes=1)
    async def tracker_tick(self):
        """Main Tracker tick

        Main tick for sending hourly charts, updating activity and updating channels
        """

        minute = dt.now().minute

        self.servers = get_servers()

        # Registering update and downtime events of a server in tempdata
        await self.register_uptime(self.servers)

        # Every five minutes or hour
        if minute % 5 == 0 or minute == 0:
            # Every five minutes
            if minute % 5 == 0:
                await self.update_channels()
            # Every hour
            if minute == 0:
                await self.send_chart()

        await self.update_activity()
        
    async def update_activity(self):
        """Simply updating bot activity
        """

        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"{all_players_count()} players in {str(len(self.servers))} servers"
            )
        )

    async def send_chart(self):
        """Sending the chart to #hourly-chart channel
        """

        MCTracker().draw_chart()

        embed = Embed(title="Hourly Track", description=f"🥇 **{self.servers[0].name}** in the lead with **{self.servers[0].current_players}** Players", color=0x00D166) #creates embed
        embed.set_footer(text=f"IRMCTracker Bot - {get_beautified_dt()}")
        file = File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        await self.bot.get_channel(Config.Channels.HOURLY).send(
            file=file, embed=embed
        )

        os.remove('chart.png')

    async def update_channels(self):
        """Updating the channels with newly fetched data

        TODO:
            - Refactor this code (Can do it with a simple for loop)
        """
        await self.bot.get_channel(Config.Channels.VC_1).edit(
            name=f"🥇 {shortified(self.servers[0].name, 10)} [{self.servers[0].current_players}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_2).edit(
            name=f"🥇 {shortified(self.servers[1].name, 10)} [{self.servers[1].current_players}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_3).edit(
            name=f"🥈 {shortified(self.servers[2].name, 10)} [{self.servers[2].current_players}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_4).edit(
            name=f"🥈 {shortified(self.servers[3].name, 10)} [{self.servers[3].current_players}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_5).edit(
            name=f"🥉 {shortified(self.servers[4].name, 10)} [{self.servers[4].current_players}👥]"
        )
        await self.bot.get_channel(Config.Channels.VC_6).edit(
            name=f"🥉 {shortified(self.servers[5].name, 10)} [{self.servers[5].current_players}👥]"
        )

        await self.bot.get_channel(Config.Channels.ALL).edit(
            name=f"💎 All Players [{all_players_count()}👥]"
        )
        await self.bot.get_channel(Config.Channels.EMPTY).edit(
            name=f"📈 Empty Count [{zero_player_servers_count()}🔨]"
        )  

    async def is_online(self, server):
        if server.latest_latency == 0:
            return False
        return True

    async def register_uptime(self, servers):            
        #setting the timestamp, depending on the latest latency, we can measure uptime and downtime of a server
        #if the downtime of a server is more than a month, then we can assume that the server is shutdown and we can remove it from the list #I'll do it later yoyoyoyo
        #new logic: tracker may or may not ping the server correctly and it sometimes happens that the tracker won't have a clear response from the server duo to anything... 
        #so we add a new tempdata variable called "strike", if the strike reaches "3", then we can assume that the serer IS OFFLINE. We only do this for offline events because
        #the chance of getting 0 latency is much higher
        for server in servers:
            is_online = await self.is_online(server)
            embed = None
            
            if not server.address in self.bot.tempdata:
                # Then the bot is restarted and no need to alert
                self.bot.tempdata[f"{server.address}"] = {"isOnline": is_online, "lastUptime": dt.now() if is_online else None, "lastDowntime": None, "strike": 0}
            else:
                server_tempdata = self.bot.tempdata[f"{server.address}"]
                previous_is_online = server_tempdata["isOnline"]
                if is_online == previous_is_online:
                    if is_online:
                        server_tempdata["lastUptime"] = dt.now()
                        #Now if the new ping latency is not "0", then we can clear the strikes here
                        self.bot.tempdata[server.address]['strike'] = 0
                    else:
                        server_tempdata["lastDowntime"] = dt.now()
                    
                else:
                    # Alert channel
                    alert_channel = self.bot.get_channel(Config.Channels.ALERTS)
                    if previous_is_online is True:
                        strikevalue = self.bot.tempdata[server.address]['strike']
                        self.bot.tempdata[server.address]['strike'] = strikevalue + 1
                        if strikevalue == 3:
                            last_downtime = server_tempdata["lastDowntime"]
                            embed = Embed(
                                title=f"\U0001f6a8 Server {server.name} offline shod!",
                                description=f"Server {server.name} lahazati pish az dastres kharej shod.",
                                color=0xff5757
                            )

                            if last_downtime:
                                final = dt.now() - last_downtime
                                final = final.total_seconds()
                                the_value = None
                                if final >= 3600:
                                    the_value = f"Aprx {round(final/3600)} hour(s)"
                                else:
                                    the_value = f"Aprx {round(final/60)} minute(s)"
                                embed.add_field(name="\U0001f550 Uptime time:", value=the_value)

                            server_tempdata["lastDowntime"] = dt.now()
                            server_tempdata["isOnline"] = False
                            self.bot.tempdata[server.address]['strike'] = 0
                    else:
                        last_uptime = server_tempdata["lastUptime"]
                        embed = Embed(
                            title=f"Server {server.name} online shod!",
                            description=f"\U0001f6a8 Server {server.name} lahazati pish online shod.",
                            color=0x00D166
                        )

                        if last_uptime:
                            final = dt.now() - last_uptime
                            final = final.total_seconds()
                            the_value = None
                            if final >= 3600:
                                the_value = f"Aprx {round(final/3600)} hour(s)"
                            else:
                                the_value = f"Aprx {round(final/60)} minute(s)"
                            embed.add_field(name="\U0001f550 Downtime time:", value=the_value)
                        
                        server_tempdata["lastUptime"] = dt.now()
                        server_tempdata["isOnline"] = True

                    self.bot.tempdata[f"{server.address}"] = server_tempdata

                    if embed != None:
                        favicon = None
                        if server.favicon_path:
                            favicon = File(server.favicon_path, filename="fav.png")
                            embed.set_thumbnail(url="attachment://fav.png")

                        embed.set_footer(text=f"IRMCTracker Bot - {get_beautified_dt()}", icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=2048')

                        await alert_channel.send(file=favicon,embed=embed)

    


def setup(client):
    client.add_cog(Tracker(client))
