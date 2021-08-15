from discord import Embed

from discord.ext.commands import Cog, command

from modules.utils import UsernameToUUID


class Skin(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BODY_BASE_URL = 'https://crafatar.com/renders/body/'
        self.HEAD_BASE_URL = 'https://crafatar.com/renders/head/'
        self.GET_ARGS = '?size=512&default=MHF_Steve&overlay'

    @command()
    async def skin(self, ctx, username = None):
        # Check if username is specified in the command
        if not username:
            embed = Embed(title="🤔 Khob alan donbale che skini hasti dabsh?", 
                            description="Usage: .skin [name] | .skin Alijk", 
                            color=0xFF0000)
            return await ctx.send(embed=embed)
        
        uuid = UsernameToUUID(username).get_uuid()

        # Check if username is valid and exists
        if uuid == '':
            embed = Embed(title=f"🤨 Nemidoonam {username} kie?!", 
                            color=0xFF0000)
            return await ctx.send(embed=embed)
        
        embed = Embed(title=f"💎 Skin of {username}", color=0x00BCD4)
        embed.set_image(url=self.BODY_BASE_URL + uuid + self.GET_ARGS)

        await ctx.send(embed=embed)
        

    @command()
    async def head(self, ctx, username = None):
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
        
        embed = Embed(title=f"💎 Head of {username}", color=0x00BCD4)
        embed.set_image(url=self.BODY_BASE_URL + uuid + self.GET_ARGS)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Skin(bot))
