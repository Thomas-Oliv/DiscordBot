
from discord.ext import commands
from Commands.HelperFunctions import *


class Admin(commands.Cog, name='Admin'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    @commands.command()
    async def DM(self, ctx, user: discord.User, *, message=None):
        message = message or "This Message is sent via DM"
        print('sending DM')
        await user.send(message)
