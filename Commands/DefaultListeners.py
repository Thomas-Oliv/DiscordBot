import logging
import math
import sys
import traceback
from discord.ext import commands,tasks
from dotenv import load_dotenv
from Functions.KeywordFunctions import pogCheck,owoCheck,uwuCheck,tiddyCheck,bootyCheck,eggplantCheck
from Functions.HelperFunctions import notifyUsers
import discord
from datetime import datetime
import os
import asyncio

logger = logging.getLogger(__name__)
load_dotenv(override=True)


class DefaultListeners(commands.Cog, name='DefaultListeners'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None
        self.notify.start()

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            print(f'{guild.name}(id: {guild.id})')
            print(f'{self.bot.user} has connected to Discord!')


    @tasks.loop(hours=1)
    async def notify(self):
        if datetime.now().hour == os.getenv('NOTIFY_HOUR'):
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            await notifyUsers(self.bot, today)
            await asyncio.sleep(3600)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if len(message.content) > 0:
            if message.content[0] != os.getenv("COMMAND_SYMBOL"):
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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # get the original exception
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{error}. Use {os.getenv("COMMAND_SYMBOL")}help to see available commands.')
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            await ctx.send(_message)
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send('This command has been disabled.')
            return

        if isinstance(error, commands.CommandOnCooldown):
            msg = await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))
            await msg.delete(delay=10)
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            msg =await ctx.send(_message)
            await msg.delete(delay=10)
            return

        if isinstance(error, commands.UserInputError):
            msg = await ctx.send(f'Invalid command parameters. Type `{os.getenv("COMMAND_SYMBOL")}help {ctx.command}` for more information.')
            await msg.delete(delay=10)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send('This command cannot be used in direct messages.')
            except discord.Forbidden:
                pass
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
            return

        # ignore all other exception types, but print them to stderr
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        print(error)
        logger.error(traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr))