

import discord
from discord.ext import commands
from Commands.HelperFunctions import *


class DefaultListeners(commands.Cog, name='DefaultListeners'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            print(f'{guild.name}(id: {guild.id})')
            print(f'{self.bot.user} has connected to Discord!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if len(message.content) > 0:
            if message.content[0] != ConfigObjects.COMMAND_PREFIX.value:
                if await pogCheck(message):
                    return
                if await eggplantCheck(message):
                    return
                if await owoCheck(message):
                    return
                if await tiddyCheck(message):
                    return
                if await bootyCheck(message):
                    return
                if await uwuCheck(message):
                    return
