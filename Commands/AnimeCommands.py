from dotenv import load_dotenv
from discord.ext import commands
from APIConnectors.AnimeConnector import AnimeConnector
from Functions.HelperFunctions import AddAnimeToList,channelcheck
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
        if not await channelcheck(ctx):
            return
        try:
            connector = MySqlAnime(os.getenv('ANIME_USER'), os.getenv('ANIME_PASSWORD'), os.getenv('ANIME_HOST'), os.getenv('ANIME_DATABASE'), os.getenv('ANIME_PORT'))
            result = connector.GetList(ctx.author.id)
            index = 0
            str_list = []
            print(result)
            if result is None or len(result) == 0:
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
        if not await channelcheck(ctx):
            return
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

    @commands.command(brief='Removes an anime based on selected index.',
                      help='1. Index: `index to be removed` (Optional)',
                      usage=f'`{os.getenv("COMMAND_SYMBOL")}remove 1`',
                      description='Note: Not specifying index will list the anime instead!\nYou can also specify \'all\' to remove all anime from your tracked list.',
                      aliases=['Remove', 'REMOVE'])
    async def remove(self, ctx, selectedIndex: str = None):
        timeout=60
        if not await channelcheck(ctx):
            return
        try:
            if selectedIndex.lower() == 'all':
                selected = -1
            else:
                selected = int(selectedIndex)
            connector = MySqlAnime(os.getenv('ANIME_USER'), os.getenv('ANIME_PASSWORD'), os.getenv('ANIME_HOST'), os.getenv('ANIME_DATABASE'), os.getenv('ANIME_PORT'))
            result = connector.GetList(ctx.author.id)
            index = 0
            selectedAnime = -1
            str_list = []
            #Check to see if user is tracking anime
            if result is None:
                await ctx.channel.send("You are not currently tracking any anime!")
            else:
                #Build output list for anime
                for (AnimeID, Title) in result:
                    if selected == index:
                        #Get selected anime's ID
                        selectedAnime = AnimeID
                    str_list.append(f'{index}. {Title}\n')
                    index += 1
                #Build anime object
                embedobj = discord.Embed(title=f'Remove an Anime', description=''.join(str_list), color=int(os.getenv("DEFAULT_COLOR")))
                if selected is not None:
                    def check(reaction, user):
                        return user.id == ctx.author.id and (str(reaction.emoji) == '✔' or str(reaction.emoji) == '❌')
                    if selectedIndex.lower() == 'all':
                        embedobj.add_field(name='To be removed', value='All')
                    #Check to see if selected index is valid
                    elif 0 <= selected < index:
                        embedobj.add_field(name='To be removed', value=str_list[selected])
                    else:
                        warn = await ctx.channel.send("Invalid index selected!")
                        await asyncio.sleep(15)
                        try:
                            await ctx.message.delete()
                        finally:
                            await warn.delete()
                            return
                    embedobj.set_footer(text='Please react to confirm removal.\nThis request will timeout in 60 seconds.')
                    messageobj = await ctx.channel.send(embed=embedobj)
                    await messageobj.add_reaction('✔')
                    await messageobj.add_reaction('❌')
                    try:
                        reactionObj, userObj = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)
                        if reactionObj.emoji == '✔':
                            if selectedIndex.lower() == 'all':
                                connector.RemoveAllAnime(ctx.author.id)
                                await ctx.channel.send(f'All tracked anime have been removed.')
                            else:
                                connector.RemoveAnime(ctx.author.id, selectedAnime)
                                await ctx.channel.send(f'Tracked Anime has been removed successfully.')
                        else:
                            raise TimeoutError()
                    except asyncio.TimeoutError:
                        try:
                            await ctx.message.delete()
                        finally:
                            await messageobj.delete()
                #else warn user
                else:
                    await ctx.channel.send(embed=embedobj)
        except Exception as ex:
            err = f'Error retrieving your anime list.'
            logger.error(f'Time: {datetime.now()} | From User: {ctx.author.name} | Command: {ctx.command} | Error: {ex} | Info: {err} | Trace: {traceback.format_exc()}')
            await ctx.channel.send(err)