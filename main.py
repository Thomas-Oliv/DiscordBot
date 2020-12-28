# bot.py
import os
import sys

import discord

from dotenv import load_dotenv
from discord.ext import commands
from ConfigObjects import ConfigObjects
from Commands.AdminCommands import Admin
from Commands.AnimeCommands import Anime
from Commands.DefaultListeners import DefaultListeners
from Commands.GamblingCommands import Gambling
load_dotenv()

def main():
    bot = commands.Bot(command_prefix=ConfigObjects.COMMAND_PREFIX.value)
    bot.add_cog(Admin(bot))
    bot.add_cog(Anime(bot))
    bot.add_cog(DefaultListeners(bot))
    bot.add_cog(Gambling(bot))
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(str(ex))
    finally:
        sys.exit(0)

