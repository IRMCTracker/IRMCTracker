from peewee import DoesNotExist
from modules.database import Server, get_servers
from modules.database import Vote as VoteDB

from discord import Embed
from discord.ext.commands import Cog, command, has_role, group

from dislash import SelectMenu, SelectOption

class Vote(Cog):
    """Voting system

    """

    def __init__(self, bot):
        self.bot = bot
        self.bot.is_voting_enabled = False
    
    @group(invoke_without_command=True, aliases=['vt'])
    @has_role('root')
    async def voting(self, ctx):
        await ctx.send('No arguments detected')

    @voting.command()
    @has_role('root')
    async def start(self, ctx):
        VoteDB.raw('DELETE FROM votes')

        servers = get_servers()

        options = []

        for server in servers:
            options.append(SelectOption(server.name, server.id))
        
        embed = Embed(title="💎 نظر سنجی بهترین سرور ماینکرفتی", 
                        description="به نظر شما کدام سرور ماینکرفتی لایق مقام 🥇 اول در ایران هستش؟\nسرور مورد نظر خودتون رو داخل باکس پایین انتخاب کنید", 
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
            values = [option.value for option in inter.select_menu.selected_options]
            
            await inter.reply(f"✅ {inter.author} نظر شما ثبت شد", delete_after=3)

            VoteDB.insert(
                user_id = inter.author.id,
                server_id= values[0]
            ).on_conflict('replace').execute()


    @voting.command()
    @has_role('root')
    async def stop(self, ctx):
        if self.bot.is_voting_enabled:
            embed = Embed(title="⭕ Stopped Voting", description="I'm no longer listening to votes", color=0xD32F2F)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Voting is not started yet!')

    @voting.command(aliases=['results', 'r'])
    @has_role('root')
    async def result(self, ctx):
        servers = get_servers()
        
        #Looping through all server in database so that 
        # we can count and sort based on votes
        for server in servers:
            # Gonna check if server has any votes,
            # if it has, we count & store them
            try:
                # Try to count server votes
                server.votes_count = len(server.votes)
            # Excepts when server doesnt have any votes so we set it to 0
            except DoesNotExist:
                server.votes_count = 0

        # Sorting servers based on votes_count (that we created in loop above)
        servers_sorted = sorted(servers, key=lambda x: x.votes_count, reverse=True)

        embed = Embed(title="💎 3 سرور برتر ایران",
                        description="3 سرور برتر ایرانی بر اساس نظرسنجی ترکر", 
                        color=0xFF9800)

        embed.add_field(name=f"🥇 مقام اول: {servers_sorted[0].name}",
                            value=f"تعداد رای: {str(servers_sorted[0].votes_count)} نفر",
                            inline=False)

        embed.add_field(name=f"🥈 مقام دوم: {servers_sorted[1].name}",
                            value=f"تعداد رای: {str(servers_sorted[1].votes_count)} نفر",
                            inline=False)

        embed.add_field(name=f"🥉 مقام سوم: {servers_sorted[2].name}",
                            value=f"تعداد رای: {str(servers_sorted[2].votes_count)} نفر",
                            inline=False)

        await ctx.send(embed=embed)

        
def setup(client):
    client.add_cog(Vote(client))
