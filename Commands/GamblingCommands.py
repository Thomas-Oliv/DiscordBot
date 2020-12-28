# bot.py
import os
from decimal import *
import discord
import random
from MySqlTransactions import MySqlTransaction
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import asyncio
from AnimeConnector import AnimeConnector
from MySqlAnime import MySqlAnime


class Gambling(commands.Cog, name = 'Gambling'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    @client.command()
    async def coinflip(ctx, typestr: str, opponent: discord.User = None):
        timeout = 60
        if typestr is None or (typestr.lower() != 'heads' and typestr.lower() != 'tails'):
            return
        if opponent is not None:
            if opponent.id == ctx.author.id or opponent.id == client.user.id:
                return

        def check(reaction, user):
            if opponent is None:
                return ((user.id != ctx.author.id and user.id != client.user.id) and str(reaction.emoji) == '✔') or (user.id == ctx.author.id and str(reaction.emoji) == '❌')
            else:
                return user.id == opponent.id and (str(reaction.emoji) == '✔' or str(reaction.emoji) == '❌')

        embedobj = discord.Embed(title=f'Coin Flip', description='Please react to this message to participate in the '
                                                                 'coinflip!', color=defaultColor)
        embedobj.set_footer(text='The user who initiated the flip can cancel by reacting with \'❌\' before'
                                 f' it has been accepted.\nNote this request will timeout after {timeout} seconds.')
        embedobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
        embedobj.add_field(name='Choice', value=typestr.lower())
        if opponent is None:
            embedobj.add_field(name='Opponent', value='Anyone')
        else:
            embedobj.add_field(name='Opponent', value=f'<@{opponent.id}>')

        messageobj = await ctx.channel.send(embed=embedobj)
        await messageobj.add_reaction("✔")
        await messageobj.add_reaction("❌")
        try:
            reactionObj, userObj = await client.wait_for("reaction_add", timeout=timeout, check=check)
            if str(reactionObj.emoji) == "✔":
                await performflip(ctx, userObj, typestr)
            else:
                await ctx.message.delete()
                await messageobj.delete()
        except asyncio.TimeoutError as error:
            print(f'Coin Flip from {ctx.author.name} has timed out')
            await ctx.message.delete()
            await messageobj.delete()

    @client.command()
    async def balance(ctx):
        connector = MySqlTransaction(os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('HOST'), os.getenv('DATABASE'), os.getenv('PORT'))
        bal = connector.GetBalance(ctx.author.id)
        if bal is None:
            await ctx.channel.send('You do not have any balance!')
        else:
            await ctx.channel.send(f'Your Balance is {(bal):.8f}!')

    @client.command()
    async def deposit(ctx, amount: Decimal, touser: discord.User = None):
        if amount <= 0:
            return
        connector = MySqlTransaction(os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('HOST'), os.getenv('DATABASE'), os.getenv('PORT'))
        if touser is None:
            currBal = connector.GetBalance(ctx.author.id)
            if currBal is None:
                connector.UpdateBalance(ctx.author.id, amount)
                await ctx.channel.send(f'{(amount):.8f} has been added to your account. Your Balance is now {amount}.')
            else:
                connector.UpdateBalance(ctx.author.id, currBal + amount)
                await ctx.channel.send(f'{(amount):.8f} has been added to your account. Your Balance is now {(currBal + amount):.8f}.')
            connector.WriteTransactionLog(ctx.author.id, amount, ctx.author.id, '')
        else:
            currBal = connector.GetBalance(touser.id)
            if currBal is None:
                connector.UpdateBalance(touser.id, amount)
            else:
                connector.UpdateBalance(touser.id, currBal + amount)
            await ctx.channel.send(f'{(amount):.8f} has been added to <@{touser.id}>\'s account.')
            connector.WriteTransactionLog(ctx.author.id, amount, touser.id, '')

    @client.command()
    async def withdraw(ctx, amount: Decimal):
        if amount <= 0:
            return
        connector = MySqlTransaction(os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('HOST'), os.getenv('DATABASE'), os.getenv('PORT'))
        currBal = connector.GetBalance(ctx.author.id)
        if currBal is not None and currBal >= amount:
            connector.UpdateBalance(ctx.author.id, currBal - amount)
            await ctx.channel.send(f'{(amount):.8f} has been withdrawn from your account. Your Balance is now {(currBal - amount):.8f}.')
            connector.WriteTransactionLog(ctx.author.id, (-amount), ctx.author.id, '')
        else:
            await ctx.channel.send('You cannot withdraw more than you have!')
            return

    @client.command()
    async def returnallbalances(ctx):
        connector = MySqlTransaction(os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('HOST'), os.getenv('DATABASE'), os.getenv('PORT'))
        allbalances = connector.ReturnAllBalances()
        str_list = []
        for (user, balance) in allbalances:
            str_list.append(f'User: <@{user}> | Balance: {balance}\n')

        await ctx.channel.send(''.join(str_list))

    @client.command()
    async def returnlogdata(ctx):
        connector = MySqlTransaction(os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('HOST'), os.getenv('DATABASE'), os.getenv('PORT'))
        allentries = connector.ReturnLog()
        str_list = []
        for (EntryTime, TransactionAmount, DiscordID, RecipientID, WalletAddress) in allentries:
            str_list.append(f'User: <@{DiscordID}> | Transaction Amount: {TransactionAmount} | Recipient: <@{RecipientID}> | Entry Time: {EntryTime} | Wallet Address: {WalletAddress}\n')
        await ctx.channel.send(''.join(str_list))