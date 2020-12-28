
from discord.ext import commands
from APIConnectors.AnimeConnector import *
from Commands.HelperFunctions import *
from ConfigObjects import ConfigObjects


class Anime(commands.Cog, name='Anime'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member_ = None

    @commands.command()
    async def GetAnimeList(self, ctx):
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
            embedobj = discord.Embed(title=f'Currently Tracked Anime', description=''.join(str_list), color=ConfigObjects.DEFAULT_COLOR.value)
            await ctx.channel.send(embed=embedobj)

    @commands.command()
    async def Search(self, ctx, *, title):
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

        embedobj = discord.Embed(title=f'Search Results', description=''.join(str_list), color=ConfigObjects.DEFAULT_COLOR.value)

        embedobj.set_footer(text=f'Note this request will timeout after {timeout} seconds.')
        embedobj.add_field(name='Requested By', value=f'<@{ctx.author.id}>')
        embedobj.add_field(name='Searched for', value=f'\"{title}\"')

        messageobj = await ctx.channel.send(embed=embedobj)
        for i in range(index):
            await messageobj.add_reaction(emojis[i])
        await messageobj.add_reaction('❌')
        try:
            reactionObj, userObj = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)
            if (reactionObj.emoji != '❌'):
                title = await AddAnimeToList(ctx.author.id, results["data"]["Page"]["media"][emojis.index(reactionObj.emoji)])
                await ctx.channel.send(f'{title} has been added.')
            else:
                await ctx.message.delete()
                await messageobj.delete()
        except asyncio.TimeoutError as error:
            print(f'Search request has timed out for {ctx.author.name}!')
            await ctx.message.delete()
            await messageobj.delete()

