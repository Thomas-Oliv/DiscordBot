import os
from datetime import  datetime

import discord
import random
import traceback

from discord.utils import get
from dotenv import load_dotenv
from py_linq import Enumerable
from MySQL.MySqlAnime import MySqlAnime
from APIConnectors.AnimeConnector import AnimeConnector
import asyncio
import logging

logger = logging.getLogger(__name__)
load_dotenv(override=True)

async def AddAnimeToList(id, selected):
    connector = MySqlAnime(os.getenv('ANIME_USER'), os.getenv('ANIME_PASSWORD'), os.getenv('ANIME_HOST'), os.getenv('ANIME_DATABASE'), os.getenv('ANIME_PORT'))
    if selected["title"]["romaji"]:
        title = selected["title"]["romaji"]
    elif selected["title"]["english"]:
        title = selected["title"]["english"]
    else:
        title = selected["title"]["native"]
    connector.AddAnime(id, selected['id'], title)
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
    else:
        result = 'Tails 😡'
        if typestr.lower() == 'tails':
            winner = ctx.author.id
        else:
            winner = opponent.id
    embedobj.set_image(url='https://i.gifer.com/789z.gif')
    await ctx.channel.send(embed=embedobj)
    resultobj = discord.Embed(title='Coin Flip Result', description=f'The winner is: <@{winner}>', color=int(os.getenv("DEFAULT_COLOR")))
    resultobj.add_field(name='Result', value=result, inline=False)
    resultobj.add_field(name='Seed', value=str(seed), inline=False)
    resultobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
    resultobj.add_field(name='Choice', value=typestr.lower())
    resultobj.add_field(name='Opponent', value=f'<@{opponent.id}>')
    await asyncio.sleep(5)
    await ctx.channel.send(embed=resultobj)
    return winner


async def notifyUsers(bot, today: float):
    connector = MySqlAnime(os.getenv('ANIME_USER'), os.getenv('ANIME_PASSWORD'), os.getenv('ANIME_HOST'), os.getenv('ANIME_DATABASE'), os.getenv('ANIME_PORT'))
    try:
        #get all tracked anime
        results = connector.getalltracked()
        #group by anime id
        for animeId in Enumerable(results).distinct(lambda x: x[0]).select(lambda x: x[0]):
            #get the anime's episodes
            anime = AnimeConnector.getepisodesbyid(animeId)['data']['Media']
            #if anime is releasing then check for new episode
            if anime['status'] == 'RELEASING':
                #check to see if there is an episode airing today
                episodeToday = Enumerable(anime['airingSchedule']['nodes']).where(lambda x: today <= x['airingAt'] <= (today + 86400)).select(lambda x: [x['episode'], x['airingAt']]).first_or_default()
                if episodeToday is not None:
                    #if an episode is airing today, notify all related users
                    for discordID in Enumerable(results).where(lambda x: x[0] == animeId).select(lambda x: x[1]):
                        user = await bot.fetch_user(discordID)
                        await user.send(f'{anime["title"]["romaji"]} has episode {episodeToday[0]} releasing at {datetime.fromtimestamp(episodeToday[1]).time()} today!')
            #delete anime from all users tracked animes
            else:
                #notify all users that the anime will be untracked
                for discordID in Enumerable(results).where(lambda x: x[0] == animeId).select(lambda x: x[1]):
                    user = bot.get_user(discordID)
                    await user.send(f'{anime["title"]["romaji"]} has finished and will no longer be tracked.')
                #untrack the anime
                connector.UntrackAnime(animeId)
    except Exception as ex:
        err = f'Error sending tracked anime'
        logger.error(f'Time: {datetime.now()} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')



async def channelcheck(ctx):
    if str(ctx.channel.category_id) != os.getenv("COMMAND_CATEGORY"):
        msg = await ctx.channel.send('You cannot use this command here.')
        await asyncio.sleep(10)
        try:
            await ctx.message.delete()
        finally:
            await msg.delete()
            return False
    else:
        return True
