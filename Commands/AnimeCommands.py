from dotenv import load_dotenv
from discord.ext import commands
from APIConnectors.AnimeConnector import AnimeConnector
from Functions.HelperFunctions import AddAnimeToList
from MySQL.MySqlAnime import MySqlAnime
import asyncio
import discord
import logging
import os
from datetime import datetime
import traceback

load_dotenv(override=True)
logger = logging.getLogger(__name__)


class Anime(commands.Cog, name='Anime'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    @commands.command(brief='Get\'s your list of tracked anime',
                      help='None',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}animelist`',
                      description='None', aliases=['AnimeList', 'ANIMELIST'])
    async def animelist(self, ctx):
        try:
            connector = MySqlAnime(os.getenv('ANIMEUSER'), os.getenv('ANIMEPASSWORD'), os.getenv('HOST'), os.getenv('ANIMEDATABASE'), os.getenv('PORT'))
            result = connector.GetList(ctx.author.id)
            index = 0
            str_list = []
            if result is None:
                await ctx.channel.send("You are not currently tracking any anime!")
            else:
                for (AnimeID, Title) in result:
                    str_list.append(f'{index}. {Title}\n')
                    index += 1
                embedobj = discord.Embed(title=f'Currently Tracked Anime', description=''.join(str_list), color=int(os.getenv("DEFAULT_COLOR")))
                await ctx.channel.send(embed=embedobj)
        except Exception as ex:
            err = f'Error retrieving your anime list.'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)

    @commands.command(brief='Searches for an active anime by name',
                      help='1. Title: `title of the anime`',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}search Boku No Hero`',
                      description='None', aliases=['SEARCH', 'Search'])
    async def search(self, ctx, *, title):
        try:
            timeout = 60
            connector = AnimeConnector()
            results = connector.Search(title)
            str_list = []
            index = 0
            emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

            def check(reaction, user):
                return user.id == ctx.author.id and (str(reaction.emoji) in emojis[0:index] or str(reaction.emoji) == '❌')

            for row in results['data']['Page']['media']:
                if (index == 10):
                    break
                else:
                    str_list.append(f'{emojis[index]}: {row["title"]["romaji"]} ({row["title"]["english"]})\n')
                    index += 1

            embedobj = discord.Embed(title=f'Search Results', description=''.join(str_list), color=int(os.getenv("DEFAULT_COLOR")))

            embedobj.set_footer(text=f'Note this request will timeout after {timeout} seconds.')
            embedobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
            embedobj.add_field(name='Searched for', value=f'\"{title}\"')

            messageobj = await ctx.channel.send(embed=embedobj)
            for i in range(index):
                await messageobj.add_reaction(emojis[i])
            await messageobj.add_reaction('❌')
            try:
                reactionObj, userObj = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)
                if reactionObj.emoji != '❌':
                    title = await AddAnimeToList(ctx.author.id, results["data"]["Page"]["media"][emojis.index(reactionObj.emoji)])
                    await ctx.channel.send(f'{title} has been added.')
                else:
                    try:
                        await ctx.message.delete()
                    finally:
                        await messageobj.delete()
            except asyncio.TimeoutError:
                try:
                    await ctx.message.delete()
                finally:
                    await messageobj.delete()
        except Exception as ex:
            err = f'Error Searching for an anime!'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)
