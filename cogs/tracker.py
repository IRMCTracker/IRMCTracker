import os
from config import get
from mcserver import MCTracker
from datetime import datetime as dt
import discord
from discord.ext import commands, tasks

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_activity_count = 1

        tracker = MCTracker()
        tracker.fetch_all()
        self.sorted_servers = tracker.sort_all()


    @tasks.loop(seconds=30.0)
    async def tracker_activity_tick(self):
        await self.update_activity()
    
    @tasks.loop(minutes=1)
    async def tracker_tick(self):
        minute = dt.now().minute


        if minute % 5 == 0 or minute == 0:
            tracker = MCTracker()
            tracker.fetch_all()
            self.sorted_servers = tracker.sort_all()

            if minute % 5 == 0:
                top1vc = self.bot.get_channel(866289711050784788)
                top2vc = self.bot.get_channel(866289915783544832)
                top3vc = self.bot.get_channel(866290014274584606)
                top4vc = self.bot.get_channel(866594448677928960)
                top5vc = self.bot.get_channel(866594475110694932)
                top6vc = self.bot.get_channel(866594488814403615)

                totalvc = self.bot.get_channel(866377410102296596)
                zerovc = self.bot.get_channel(866377830089621504)

                await top1vc.edit(name=f"🥇 {self.sorted_servers[0].get_name()} [{self.sorted_servers[0].get_online_players()}👥]")
                await top2vc.edit(name=f"🥇 {self.sorted_servers[1].get_name()} [{self.sorted_servers[1].get_online_players()}👥]")
                await top3vc.edit(name=f"🥈 {self.sorted_servers[2].get_name()} [{self.sorted_servers[2].get_online_players()}👥]")
                await top4vc.edit(name=f"🥈 {self.sorted_servers[3].get_name()} [{self.sorted_servers[3].get_online_players()}👥]")
                await top5vc.edit(name=f"🥉 {self.sorted_servers[4].get_name()} [{self.sorted_servers[4].get_online_players()}👥]")
                await top6vc.edit(name=f"🥉 {self.sorted_servers[5].get_name()} [{self.sorted_servers[5].get_online_players()}👥]")

                await totalvc.edit(name=f"💎 All Players [{tracker.all_player_count()}👥]")
                await zerovc.edit(name=f"📈 Empty Count [{tracker.zero_player_count()}🔨]")
            if minute == 0:
                tracker.draw_chart()
                
                hourly_channel = self.bot.get_channel(866288509269966878)

                embed = discord.Embed(title="Hourly Track", description=f"🥇 **{self.sorted_servers[0].get_name()}** in the lead with **{self.sorted_servers[0].get_online_players()}** Players", color=0x00D166) #creates embed
                embed.set_footer(text=f"IRMCTracker Bot - {dt.now():%Y-%m-%d %I:%M:%S}")
                file = discord.File("chart.png", filename="chart.png")
                embed.set_image(url="attachment://chart.png")
                await hourly_channel.send(file=file, embed=embed)

                os.remove('chart.png')

    @commands.command()
    async def sendhourly(self,ctx):
        if ctx.author.id != 296565827115941889:
            return

        tracker = MCTracker()
        tracker.fetch_all()
        sorted_servers = tracker.sort_all()

        tracker.draw_chart()
                
        hourly_channel = self.bot.get_channel(866288509269966878)

        embed = discord.Embed(title="Hourly Track", description=f"🥇 **{sorted_servers[0].get_name()}** in the lead with **{sorted_servers[0].get_online_players()}** Players", color=0x00D166) #creates embed
        embed.set_footer(text=f"IRMCTracker Bot - {dt.now():%Y-%m-%d %I:%M:%S}")
        file = discord.File("chart.png", filename="chart.png")
        embed.set_image(url="attachment://chart.png")
        await hourly_channel.send(file=file, embed=embed)

        os.remove('chart.png')
    

    async def update_activity(self):
        print('yas')
        await self.bot.wait_until_ready()

        if self.current_activity_count == 1:
            await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, name=f"🥇 {self.sorted_servers[0].get_name()} [{self.sorted_servers[0].get_online_players()}👥]"
                    )
                )
            self.current_activity_count += 1
        if self.current_activity_count == 2:
            await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, name=f"🥈 {self.sorted_servers[1].get_name()} [{self.sorted_servers[1].get_online_players()}👥"
                    )
                )
            self.current_activity_count += 1
        if self.current_activity_count == 3:
            await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, name=f"🥉 {self.sorted_servers[2].get_name()} [{self.sorted_servers[2].get_online_players()}👥]"
                    )
                )
            self.current_activity_count = 1

    @commands.command()
    async def updatechannels(self,ctx):
        if ctx.author.id != 296565827115941889:
            return
            
        tracker = MCTracker()
        tracker.fetch_all()
        sorted_servers = tracker.sort_all()

        top1vc = self.bot.get_channel(866289711050784788)
        top2vc = self.bot.get_channel(866289915783544832)
        top3vc = self.bot.get_channel(866290014274584606)
        top4vc = self.bot.get_channel(866594448677928960)
        top5vc = self.bot.get_channel(866594475110694932)
        top6vc = self.bot.get_channel(866594488814403615)

        totalvc = self.bot.get_channel(866377410102296596)
        zerovc = self.bot.get_channel(866377830089621504)

        await top1vc.edit(name=f"🥇 {sorted_servers[0].get_name()} [{sorted_servers[0].get_online_players()}👥]")
        await top2vc.edit(name=f"🥇 {sorted_servers[1].get_name()} [{sorted_servers[1].get_online_players()}👥]")
        await top3vc.edit(name=f"🥈 {sorted_servers[2].get_name()} [{sorted_servers[2].get_online_players()}👥]")
        await top4vc.edit(name=f"🥈 {sorted_servers[3].get_name()} [{sorted_servers[3].get_online_players()}👥]")
        await top5vc.edit(name=f"🥉 {sorted_servers[4].get_name()} [{sorted_servers[4].get_online_players()}👥]")
        await top6vc.edit(name=f"🥉 {sorted_servers[5].get_name()} [{sorted_servers[5].get_online_players()}👥]")

        await totalvc.edit(name=f"💎 All Players [{tracker.all_player_count()}👥]")
        await zerovc.edit(name=f"📈 Empty Count [{tracker.zero_player_count()}🔨]")
    
def setup(client):
    client.add_cog(Tracker(client))
