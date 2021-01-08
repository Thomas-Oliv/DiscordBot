# bot.py
from Functions.HelperFunctions import channelcheck, performflip
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import traceback
import os
import discord
import asyncio
import logging
import hashlib
import quantumrandom
import random
load_dotenv(override=True)
logger = logging.getLogger(__name__)

class Gambling(commands.Cog, name='Gambling'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    @commands.command(brief='Returns the hash for the inputted seed to validate result.',
                      help='1. Seed: `integer value for seed`',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}gethash 123`',
                      description='Note the hashing uses SHA256. Feel free to validate your results elsewhere.', aliases=['GetHash', 'GETHASH'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gethash(self, ctx, seed: int):
        if not await channelcheck(ctx):
            return
        embedobj = discord.Embed(title=f'Hash Result',
                                 description=f'The hash for {seed} is {hashlib.sha256(str(seed).encode()).hexdigest()}',
                                 color=int(os.getenv("DEFAULT_COLOR")))
        await ctx.channel.send(embed=embedobj)

    @commands.command(brief='Coin flip between two people.',
                      help=f'1. Choice: `heads` or `tails`\n2. Opponent: `@user` (Optional)',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}coinflip heads @Bot`',
                      description=f'Not specifying opponent will allow anyone to join the flip.',
                      aliases=['cf', 'CoinFlip', 'COINFLIP'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinflip(self, ctx, typestr: str, opponent: discord.User = None):
        if not await channelcheck(ctx):
            return
        try:
            timeout = 60
            if typestr is None or (typestr.lower() != 'heads' and typestr.lower() != 'tails'):
                return
            if opponent is not None:
                if opponent.id == ctx.author.id or opponent.id == self.bot.user.id:
                    return

            def check(reaction, user):
                if opponent is None:
                    return ((user.id != ctx.author.id and user.id != self.bot.user.id) and str(reaction.emoji) == '✔') or (user.id == ctx.author.id and str(reaction.emoji) == '❌')
                else:
                    return user.id == opponent.id and (str(reaction.emoji) == '✔' or str(reaction.emoji) == '❌')

            seed = quantumrandom.uint16(array_length=1)[0]
            hashval = hashlib.sha256(str(seed).encode()).hexdigest()
            embedobj = discord.Embed(title=f'Coin Flip', description='Please react to this message to participate in the '
                                                                     'coinflip!', color=int(os.getenv("DEFAULT_COLOR")))
            embedobj.set_footer(text='The user who initiated the flip can cancel by reacting with \'❌\' before'
                                     f' it has been accepted.\nNote this request will timeout after {timeout} seconds.')
            embedobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
            embedobj.add_field(name='Choice', value=typestr.lower())
            if opponent is None:
                embedobj.add_field(name='Opponent', value='Anyone')
            else:
                embedobj.add_field(name='Opponent', value=f'<@{opponent.id}>')
            embedobj.add_field(name='Hashed Seed', value=hashval)
            messageobj = await ctx.channel.send(embed=embedobj)
            await messageobj.add_reaction("✔")
            await messageobj.add_reaction("❌")
            try:
                reactionObj, userObj = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)
                if str(reactionObj.emoji) == "✔":
                    await performflip(ctx, userObj, typestr, seed)
                else:
                    try:
                        await ctx.message.delete()
                    finally:
                        await messageobj.delete()
            except asyncio.TimeoutError as error:
                print(f'Coin Flip from {ctx.author.name} has timed out')
                try:
                    await ctx.message.delete()
                finally:
                    await messageobj.delete()
        except Exception as ex:
            err = f'Error flipping the coin.'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Choice: {typestr}  | Opponent: {opponent.name} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)

    @commands.command(brief='Roll a dice!',
                      help=f'None',
                      usage=f'`None',
                      description=f'None',
                      aliases=['ROLL', 'Roll'])
    async def roll(self, ctx, dice: str):
        if not await channelcheck(ctx):
            return
        try:
            dicesplit = dice.split('d', 1)
            if len(dicesplit) == 2:
                try:
                    amount = int(dicesplit[0])
                    size = int(dicesplit[1])
                    if amount <=0 or size <=0:
                        raise ValueError('Invalid dice defined!')
                    print(f'amount: {amount} | size: {size}')
                except ValueError as ex:
                    err = f'Invalid dice defined!'
                    await ctx.channel.send(err)
                    return
                str_list = []
                total = 0
                embed = discord.Embed(title=f'{dice} Dice Roll',color=int(os.getenv("DEFAULT_COLOR")))
                for count in range(0, amount):
                    seed = quantumrandom.uint16(array_length=1)[0]
                    random.seed(seed)
                    val = random.randint(1, size)
                    str_list.append(val)
                    total += val
                if len(str_list) > 15:
                    desc = '('
                    for i in range(0, 15):
                        if (str_list[i] == 1 or str_list[i] == size):
                            desc += f' **{str_list[i]}**,'
                        else:
                            desc += f' {str_list[i]},'
                    desc = desc[:-1] + ' ...)'
                    embed.set_footer(text='Results have been trimmed for formatting.')
                else:
                    desc ='('
                    for i in range(0, len(str_list)):
                        if(str_list[i] == 1 or str_list[i] ==size ):
                            desc += f' **{str_list[i]}**,'
                        else:
                            desc += f' {str_list[i]},'
                    desc = desc[:-1] + ')'
                embed.add_field(name='Result',value=desc, inline=False)
                embed.add_field(name='Total', value=str(total), inline=False)
                await ctx.channel.send(embed=embed)
        except Exception as ex:
            err = f'Error Rolling the dice'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)