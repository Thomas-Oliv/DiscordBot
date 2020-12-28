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
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
commandPrefix = '!'
client = commands.Bot(command_prefix=commandPrefix)
defaultColor = 0x000080


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')
        print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message : discord.Message):
    if message.author == client.user:
        return
    if len(message.content)>0:
        if message.content[0] == commandPrefix:
            await client.process_commands(message)
            return
        else:

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

@client.command()
async def DM(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    print('sending DM')
    await user.send(message)

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
            connector.UpdateBalance(ctx.author.id, currBal+amount)
            await ctx.channel.send(f'{(amount):.8f} has been added to your account. Your Balance is now {(currBal+amount):.8f}.')
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
        connector.UpdateBalance(ctx.author.id, currBal-amount)
        await ctx.channel.send(f'{(amount):.8f} has been withdrawn from your account. Your Balance is now {(currBal-amount):.8f}.')
        connector.WriteTransactionLog(ctx.author.id, (-amount), ctx.author.id, '')
    else:
        await ctx.channel.send('You cannot withdraw more than you have!')
        return

@client.command()
async def returnallbalances(ctx):
    connector =  MySqlTransaction(os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('HOST'), os.getenv('DATABASE'), os.getenv('PORT'))
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

@client.command()
async def GetAnimeList(ctx):
    connector = MySqlAnime(os.getenv('ANIMEUSER'), os.getenv('ANIMEPASSWORD'), os.getenv('HOST'), os.getenv('ANIMEDATABASE'), os.getenv('PORT'))
    result = connector.GetList(ctx.author.id)
    index =0
    str_list = []
    if result is None:
        await ctx.channel.send("You are not currently tracking any anime!")
    else:
        for (AnimeID,Title) in result:
            str_list.append(f'{index}. {Title}\n')
            index += 1
        embedobj = discord.Embed(title=f'Currently Tracked Anime', description=''.join(str_list), color=defaultColor)
        await ctx.channel.send(embed=embedobj)


@client.command()
async def Search(ctx, *, title):
    timeout =60
    connector = AnimeConnector()
    results = connector.Search(title)
    str_list = []
    index = 0
    emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    def check(reaction, user):
        return user.id == ctx.author.id and (str(reaction.emoji) in emojis[0:index] or str(reaction.emoji) == '❌')
    for row in results['data']['Page']['media']:
        if(index == 10):
            break;
        else:
            str_list.append(f'{emojis[index]}: {row["title"]["romaji"]} ({row["title"]["english"]})\n')
            index += 1

    embedobj = discord.Embed(title=f'Search Results', description=''.join(str_list), color=defaultColor)

    embedobj.set_footer(text=f'Note this request will timeout after {timeout} seconds.')
    embedobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
    embedobj.add_field(name='Searched for', value=f'\"{title}\"')

    messageobj = await ctx.channel.send(embed=embedobj)
    for i in range(index):
        await messageobj.add_reaction(emojis[i])
    await messageobj.add_reaction('❌')
    try:
        reactionObj, userObj = await client.wait_for("reaction_add", timeout=timeout, check=check)
        if(reactionObj.emoji != '❌'):
            title = await AddAnimeToList(ctx.author.id,results["data"]["Page"]["media"][emojis.index(reactionObj.emoji)])
            await ctx.channel.send(f'{title} has been added.')
        else:
            await ctx.message.delete()
            await messageobj.delete()
    except asyncio.TimeoutError as error:
        print(f'Search request has timed out for {ctx.author.name}!')
        await ctx.message.delete()
        await messageobj.delete()


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

async def AddAnimeToList(id, selected):
    sqlConnection = MySqlAnime(os.getenv('ANIMEUSER'), os.getenv('ANIMEPASSWORD'), os.getenv('HOST'), os.getenv('ANIMEDATABASE'), os.getenv('PORT'))
    if selected["title"]["romaji"]:
        title = selected["title"]["romaji"]
    elif selected["title"]["english"]:
        title = selected["title"]["english"]
    else:
        title = selected["title"]["native"]
    sqlConnection.AddAnime(id, selected['id'], title)
    return title




async def performflip(ctx, opponent : discord.User = None, typestr: str = None):
    random.seed(datetime.now().timestamp())
    val = random.randint(0, 1)
    print(f'flipping coin for user: {ctx.author.name} and {opponent.name}')
    if val == 1:
        embedobj=discord.Embed(
            title="Flipping the coin...",
            color=defaultColor)
        embedobj.set_image(url='https://cdn.discordapp.com/attachments/698941056007536660/787849610286202890/brwn_or_heads_wins.gif')
        await ctx.channel.send(embed=embedobj)
        resultmsg = f"And the result is... Heads 🤤"
    else:
        embedobj = discord.Embed(
            title="Flipping the coin...",
            color=defaultColor)
        embedobj.set_image(url='https://cdn.discordapp.com/attachments/698941056007536660/787849584134848572/doge_or_tails_wins.gif')
        await ctx.channel.send(embed=embedobj)
        resultmsg = f"And the result is... Tails 😡"

    resultobj = discord.Embed(title='Coin Flip Result', description=resultmsg, color=defaultColor)
    resultobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
    resultobj.add_field(name='Choice', value=typestr.lower())
    resultobj.add_field(name='Opponent', value=f'<@{opponent.id}>')
    await asyncio.sleep(3)
    await ctx.channel.send(embed=resultobj)

async def pogCheck(message):
    if message.content.lower().find('pog') >= 0:
        embedobj=discord.Embed(
            title='Pog Fish',
            description=f'<@{message.author.id}> This fish really do be pogging tho 😳',
            url='https://tenor.com/view/pog-fish-fish-mouth-open-gif-17487624',
            color=defaultColor)
        embedobj.set_image(url="https://media.tenor.com/images/30e1029fd63cb44bdb22e721d8454792/tenor.gif")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False

async def eggplantCheck(message):
    if message.content.lower().find('🍆') >= 0:
        embedobj=discord.Embed(
            description=f'Nice Cock <@{message.author.id}> 💦',
            url='https://media.tenor.com/images/1a203396cd38ee4230821bae44968d16/tenor.gif?itemid=19449051',
            color=defaultColor)
        embedobj.set_image(url="https://media.tenor.com/images/1a203396cd38ee4230821bae44968d16/tenor.gif?itemid=19449051")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False

async def owoCheck(message):
    if message.content.lower().find('owo') >= 0:
        embedobj=discord.Embed(
            title='Hewwo!',
            description=f'OwO <@{message.author.id}>',
            url='https://media.tenor.com/images/af163ddef5fff33cd244664f595fe105/tenor.gif?itemid=10868030',
            color=defaultColor)
        embedobj.set_image(url="https://media.tenor.com/images/af163ddef5fff33cd244664f595fe105/tenor.gif?itemid=10868030")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False

async def tiddyCheck(message):
    if message.content.lower().find('tiddy') >= 0:
        embedobj=discord.Embed(
            url='https://media.tenor.com/images/b2f6428fa396370c7b0c4307f9a3c654/tenor.gif?itemid=15526960',
            color=defaultColor)
        embedobj.set_image(url="https://media.tenor.com/images/b2f6428fa396370c7b0c4307f9a3c654/tenor.gif?itemid=15526960")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False

async def bootyCheck(message):
    if message.content.lower().find('booty') >= 0:
        embedobj=discord.Embed(
            url='https://media.tenor.com/images/c5278a9c6fd1d734e62dc857186efef3/tenor.gif?itemid=14892145',
            color=defaultColor)
        embedobj.set_image(url="https://media.tenor.com/images/c5278a9c6fd1d734e62dc857186efef3/tenor.gif?itemid=14892145")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False

async def uwuCheck(message):
    if message.content.lower().find('uwu') >= 0:
        embedobj=discord.Embed(
            description=f'UwU <@{message.author.id}>',
            url='https://cdn.discordapp.com/attachments/784828904136376340/792647300065001502/unknown.gif',
            color=defaultColor)
        embedobj.set_image(url="https://cdn.discordapp.com/attachments/784828904136376340/792647300065001502/unknown.gif")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False



client.run(TOKEN)