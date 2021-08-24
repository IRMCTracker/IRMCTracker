from discord import Embed
from discord.enums import Status

from discord.ext.commands import Cog, command

from modules.api.hypixel import HypixelPlayer
from modules.api import Player
from modules.utils import *

from random import randint

class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['prof','p','player'])
    async def profile(self, ctx, username:str = None):
        # Check if username is specified in the command
        if not username:
            embed = Embed(title="🤔 Khob alan donbale kale ki hasti dabsh?", 
                            description="Usage: .head [name] | .head Alijk", 
                            color=0xFF0000)
            return await ctx.send(embed=embed)
        
        player = Player(username)
        hypixel = HypixelPlayer(username)
        hypixel_player = hypixel.get_player()
        hypixel_status = hypixel.get_status()

        # Check if username is valid and exists
        if not player.is_valid():
            embed = Embed(title=f"🤨 Nemidoonam {username} kie?!", 
                            color=0xFF0000)
            return await ctx.send(embed=embed)

        embed = Embed(
            title=f"👤 Profile {username.capitalize()}", 
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(
            url=player.get_head_image()
        )

        embed.set_footer(
            text=f"IRMCTracker", 
            icon_url='https://cdn.discordapp.com/avatars/866290840426512415/06e4661be6886a7818e5ce1d09fa5709.webp?size=2048'
        )

        embed.add_field(
            name="🔗 Played on Hypixel?",
            value="🟢 Yes" if hypixel_player else "🔴 No",
            inline=False
        )

        if hypixel_player:
            embed.add_field(
                name="➕ Hypixel First Join",
                value=timestamp_ago(hypixel_player['player']['firstLogin']),
                inline=True
            )
            
            embed.add_field(
                name="⭕ Hypixel Last Played",
                value=timestamp_ago(hypixel_player['player']['lastLogin']),
                inline=True
            )

            embed.add_field(
                name="💢 Last Game Played",
                value=str(hypixel_player['player']['mostRecentGameType']).lower().capitalize(),
                inline=False
            )

            embed.add_field(
                name="💫 BedWars Level",
                value=hypixel_player['player']['achievements']['bedwars_level'],
                inline=True
            )

            embed.add_field(
                name="🔪 BedWars Wins",
                value=hypixel_player['player']['achievements']['bedwars_wins'],
                inline=True
            )

            embed.add_field(
                name="🆚 Version",
                value=hypixel_player['player']['mcVersionRp'],
                inline=False
            )

            is_online = hypixel_status['online']
            embed.add_field(
                name="✔ Is Online?",
                value='✅ Online' if is_online else '❌ Offline',
                inline=True
            )
            
            if is_online:
                embed.add_field(
                    name="🕳 Now playing",
                    value=str(hypixel_status['mode']).capitalize(),
                    inline=True
                )

        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Profile(bot))
