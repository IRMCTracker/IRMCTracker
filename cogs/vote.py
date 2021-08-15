from modules.database import *

from discord import Embed
from discord.ext.commands import Cog, command, has_role

from dislash import SelectMenu, SelectOption

class Vote(Cog):
    """Voting system

    """

    def __init__(self, bot):
        self.bot = bot
        self.bot.is_voting_enabled = False
    
    @command()
    @has_role('root')
    async def startvote(self, ctx):
        servers = get_servers()

        options = []

        for server in servers:
            options.append(SelectOption(server.name, server.name))
        
        embed = Embed(title="💎 نظر سنجی بهترین سرور ماینکرفتی", 
                        description="به نظر شما کدام سرور ماینکرفتی لایق مقام 🥇 اول در ایران هستش؟", 
                        color=0x4CAF50)

        msg = await ctx.send(
            embed=embed,
            components=[
                SelectMenu(
                    custom_id="best_server",
                    placeholder="سرور مورد نظر خودتون رو انتخاب کنید",
                    max_values=1,
                    options=options
                )
            ]
        )

        self.bot.is_voting_enabled = True

        while self.bot.is_voting_enabled:
            inter = await msg.wait_for_dropdown()

            labels = [option.label for option in inter.select_menu.selected_options]
            
            await inter.reply(f"✅ {inter.author.mention} نظر شما ثبت شد", delete_after=4)

            Vote.replace(
                user_id = inter.author.id,
                vote = labels[0]
            )


    @command()
    @has_role('root')
    async def stopvote(self, ctx):
        if self.bot.is_voting_enabled:
            embed = Embed(title="⭕ Stopped Voting", description="I'm no longer listening to votes", color=0xD32F2F)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Voting is not started yet!')

def setup(client):
    client.add_cog(Vote(client))
