from discord.ext import commands
import discord
from datetime import datetime
import asyncio
import logging
import traceback
import os
from Functions.HelperFunctions import channelcheck
from dotenv import load_dotenv

load_dotenv(override=True)
logger = logging.getLogger(__name__)

class Helper(commands.Cog, name='Helper'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    @commands.command(aliases=['Help', 'HELP'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, args=None):
        if not await channelcheck(ctx):
            return
        try:
            timeout = 60
            help_embed = discord.Embed(title="Help Menu", color=int(os.getenv("DEFAULT_COLOR")))
            command_names_list = [x.name for x in self.bot.commands]

            # If there are no arguments, just list the commands:
            if not args:
                help_embed.add_field(
                    name="List of supported commands:",
                    value="\n".join([str(i + 1) + ". " + x.name for i, x in enumerate(self.bot.commands)]),
                    inline=False
                )
                help_embed.add_field(
                    name="Details",
                    value=f'Type `{os.getenv("COMMAND_SYMBOL")}help <command name>` for more details about each command.',
                    inline=False
                )
            elif args == 'help':
                help_embed.description = 'Bruh'
            # If the argument is a command, get the help text from that command:
            elif args in command_names_list:
                cmd = self.bot.get_command(args)
                help_embed.add_field(
                    name='Command',
                    value=args,
                    inline=False
                )
                help_embed.add_field(
                    name='Description',
                    value=cmd.brief,
                    inline=False
                )
                help_embed.add_field(
                    name='Parameters',
                    value=cmd.help,
                    inline=False
                )
                help_embed.add_field(
                    name='Additional Info',
                    value=cmd.description,
                    inline=False
                )
                help_embed.add_field(
                    name='Example',
                    value=cmd.usage,
                    inline=False
                )
                if cmd.aliases is not None:
                    al = []
                    for alias in cmd.aliases:
                        al.append(f'`{alias}` ')
                    help_embed.add_field(
                        name='Aliases',
                        value=''.join(al).strip(),
                        inline=False
                    )
            # If someone is just trolling:
            else:
                help_embed.add_field(
                    name="Error",
                    value=f"command `{args}` does not exist."
                )
            help_embed.set_footer(text=f'This message will delete after {timeout} seconds.')
            msg = await ctx.channel.send(embed=help_embed)
            await asyncio.sleep(timeout)
            await msg.delete()
            try:
                await ctx.message.delete()
            except discord.NotFound:
                return
        except Exception as ex:
            err = 'Error getting help'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)
            return