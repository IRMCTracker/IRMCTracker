from nextcord import Message, Embed
from nextcord.ext.commands import command, Cog

from modules.utils import *

class Moderation(Cog):
    """Simple moderation handlers for tracker bot

    TODO:
        - Anti flood spam implementation
    """
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user or message.author.id == 296565827115941889:
            return

        warn = None

        if has_link(message.content):
            warn = 'Lotfan az ersal hargoone link khoddari konid!'
        elif has_discord_link(message.content):
            warn = 'Lotfan az ersal invite discord khoddari konid!'
        
        if warn:
            embed = Embed(title=f"{message.author.name} , {warn}", color=0xc62828, timestamp=get_utc())
            await message.channel.send(message.author.mention, embed=embed, delete_after=5.0)
            await message.delete()
            


def setup(bot):
    bot.add_cog(Moderation(bot))
