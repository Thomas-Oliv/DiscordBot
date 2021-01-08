
from discord.ext import commands
import os
from datetime import datetime
from discord.utils import get
import logging
import traceback

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv(override=True)

class Debug(commands.Cog, name='Debug'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    async def cog_check(self, ctx):
        admin = get(ctx.guild.roles, name="Debug")
        return admin in ctx.author.roles

    @commands.command(brief='Throws an Exception. (For testing log)',
                      help='None',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}throwerror`',
                      description='None',
                      aliases=['ThrowError', 'THROWERROR', 'ERROR', 'Error', 'error'])
    async def throwerror(self, ctx):
        try:
            raise Exception('Sample Error')
        except Exception as ex:
            err = f'Test Error'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)
            return

    @commands.command(brief='Gets a channel\'s ID',
                      help='None',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}category`',
                      description='None',
                      aliases=['Category', 'CATEGORY'])
    async def category(self, ctx):
        await ctx.channel.send(f'Category ID: {ctx.channel.category_id}')
