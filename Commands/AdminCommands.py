from dotenv import load_dotenv
import logging
import discord
import traceback
import os
from datetime import datetime
from Functions.HelperFunctions import channelcheck
import asyncio
from discord.ext import commands
from discord.utils import get
logger = logging.getLogger(__name__)
load_dotenv(override=True)

class Admin(commands.Cog, name='Admin'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    async def cog_check(self, ctx):
        admin = get(ctx.guild.roles, name="Admin")
        return admin in ctx.author.roles

    @commands.command(brief='DM\'s a user through the bot (For administrator purposes)',
                      help='1. To User: `@User`\nMessage: `Message to be sent`',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}dm @User Hello`',
                      description='None', aliases=['DM'])
    async def dm(self, ctx, user: discord.User, *, message=None):
        if not await channelcheck(ctx):
            return
        message = message or "This Message is sent via DM"
        await user.send(message)


    @commands.command(brief='Safely shutdown the bot',
                      help='None',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}shutdown`',
                      description='None', aliases=['SHUTDOWN', 'Shutdown'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shutdown(self, ctx):
        if not await channelcheck(ctx):
            return
        try:
            await ctx.channel.send(f"The bot will be shutting down for maintenance shortly. Commands are being locked.")
            for command in self.bot.commands:
                command.update(enabled=False)
            await ctx.channel.send(f"Shutting Down...")
        except Exception as ex:
            err = f'Error shutting down the bot'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Error: {ex} | Info: {err}  | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)
            for command in self.bot.commands:
                command.update(enabled=True)
            return
        await self.bot.logout()
        exit(0)