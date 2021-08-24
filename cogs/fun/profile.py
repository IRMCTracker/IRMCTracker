from discord import Embed

from discord.ext.commands import Cog, command

from modules.utils import UsernameToUUID


class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['prof','p','player'])
    async def profile(self, ctx, username = None):
        # Check if username is specified in the command
        if not username:
            embed = Embed(title="🤔 Khob alan donbale kale ki hasti dabsh?", 
                            description="Usage: .head [name] | .head Alijk", 
                            color=0xFF0000)
            return await ctx.send(embed=embed)
        
        uuid = UsernameToUUID(username).get_uuid()

        # Check if username is valid and exists
        if uuid == '':
            embed = Embed(title=f"🤨 Nemidoonam {username} kie?!", 
                            color=0xFF0000)
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
