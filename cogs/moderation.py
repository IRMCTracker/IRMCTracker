from discord import Message, Embed
from discord.ext.commands import command, Cog

from modules.utils import has_link, has_discord_link, message_has_mentions

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
            await message.delete()
        elif has_discord_link(message.content):
            warn = 'Lotfan az ersal invite discord khoddari konid!'
            await message.delete()
        elif message_has_mentions(message):
            warn = 'Lotfan kasi ro dakhele chat ha mention nakonid!'
            await message.delete()
        
        if warn:
            embed = Embed(title=f"{message.author.name} , {warn}", color=0xc62828)
            await message.channel.send(message.author.mention, embed=embed, delete_after=5.0)
            


def setup(bot):
    bot.add_cog(Moderation(bot))
