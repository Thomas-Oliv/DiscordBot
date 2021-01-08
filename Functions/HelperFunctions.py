import os
import discord
import random
from MySQL.MySqlAnime import MySqlAnime
import asyncio


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


async def performflip(ctx, opponent: discord.User, typestr: str, seed: int):
    random.seed(seed)
    val = random.randint(0, 1)
    embedobj = discord.Embed(
        title="Flipping the coin...",
        color=int(os.getenv("DEFAULT_COLOR")))
    if val == 1:
        result = 'Heads 🤤'
        if typestr.lower() == 'heads':
            winner = ctx.author.id
        else:
            winner = opponent.id
        embedobj.set_image(url='https://cdn.discordapp.com/attachments/698941056007536660/787849610286202890/brwn_or_heads_wins.gif')
        await ctx.channel.send(embed=embedobj)
    else:
        result = 'Tails 😡'
        if typestr.lower() == 'tails':
            winner = ctx.author.id
        else:
            winner = opponent.id
        embedobj.set_image(url='https://cdn.discordapp.com/attachments/698941056007536660/787849584134848572/doge_or_tails_wins.gif')
        await ctx.channel.send(embed=embedobj)
    resultobj = discord.Embed(title='Coin Flip Result', description=f'The winner is: <@{winner}>', color=int(os.getenv("DEFAULT_COLOR")))
    resultobj.add_field(name='Result', value=result)
    resultobj.add_field(name='Seed', value=str(seed))
    resultobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
    resultobj.add_field(name='Choice', value=typestr.lower())
    resultobj.add_field(name='Opponent', value=f'<@{opponent.id}>')
    await asyncio.sleep(3)
    await ctx.channel.send(embed=resultobj)
    return winner
