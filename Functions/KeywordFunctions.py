import discord
import os

async def pogCheck(message):
    if message.content.lower().find('pog') >= 0:
        embedobj=discord.Embed(
            title='Pog Fish',
            description=f'<@{message.author.id}> This fish really do be pogging tho 😳',
            url='https://tenor.com/view/pog-fish-fish-mouth-open-gif-17487624',
            color=int(os.getenv("DEFAULT_COLOR")))
        embedobj.set_image(url="https://media.tenor.com/images/30e1029fd63cb44bdb22e721d8454792/tenor.gif")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False

async def eggplantCheck(message):
    if message.content.lower().find('🍆') >= 0:
        embedobj = discord.Embed(
            description=f'Nice Cock <@{message.author.id}> 💦',
            url='https://media.tenor.com/images/1a203396cd38ee4230821bae44968d16/tenor.gif?itemid=19449051',
            color=int(os.getenv("DEFAULT_COLOR")))
        embedobj.set_image(url="https://media.tenor.com/images/1a203396cd38ee4230821bae44968d16/tenor.gif?itemid=19449051")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False
async def eggplantCheck(message):
    if message.content.lower().find('🍆') >= 0:
        embedobj=discord.Embed(
            description=f'Nice Cock <@{message.author.id}> 💦',
            url='https://media.tenor.com/images/1a203396cd38ee4230821bae44968d16/tenor.gif?itemid=19449051',
            color=int(os.getenv("DEFAULT_COLOR")))
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
            color=int(os.getenv("DEFAULT_COLOR")))
        embedobj.set_image(url="https://media.tenor.com/images/af163ddef5fff33cd244664f595fe105/tenor.gif?itemid=10868030")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False


async def tiddyCheck(message):
    if message.content.lower().find('tiddy') >= 0:
        embedobj=discord.Embed(
            url='https://media.tenor.com/images/b2f6428fa396370c7b0c4307f9a3c654/tenor.gif?itemid=15526960',
            color=int(os.getenv("DEFAULT_COLOR")))
        embedobj.set_image(url="https://media.tenor.com/images/b2f6428fa396370c7b0c4307f9a3c654/tenor.gif?itemid=15526960")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False


async def bootyCheck(message):
    if message.content.lower().find('booty') >= 0:
        embedobj=discord.Embed(
            url='https://media.tenor.com/images/c5278a9c6fd1d734e62dc857186efef3/tenor.gif?itemid=14892145',
            color=int(os.getenv("DEFAULT_COLOR")))
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
            color=int(os.getenv("DEFAULT_COLOR")))
        embedobj.set_image(url="https://cdn.discordapp.com/attachments/784828904136376340/792647300065001502/unknown.gif")
        await message.channel.send(embed=embedobj)
        return True
    else:
        return False
