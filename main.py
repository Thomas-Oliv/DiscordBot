# bot.py
import logging

from dotenv import load_dotenv
from Commands.AnimeCommands import Anime
import os
import sys
import logging
from dotenv import load_dotenv
from discord.ext import commands
from logging.handlers import TimedRotatingFileHandler
from Commands.AdminCommands import Admin
from Commands.DefaultListeners import DefaultListeners
from Commands.GamblingCommands import Gambling
from Commands.DebugCommands import Debug
from Commands.HelpCommands import Helper

load_dotenv(override=True)
logger = logging.getLogger()

def main():
    bot = commands.Bot(command_prefix=os.getenv("COMMAND_SYMBOL"), help_command=None)
    logger.setLevel(logging.INFO)
    output_file_handler = TimedRotatingFileHandler(f'datalog.log', when="midnight", interval=1)
    output_file_handler.prefix = "%Y%m%d"
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stdout_handler)
    logger.addHandler(output_file_handler)
    bot.add_cog(Admin(bot))
    bot.add_cog(Anime(bot))
    bot.add_cog(Debug(bot))
    bot.add_cog(DefaultListeners(bot))
    bot.add_cog(Gambling(bot))
    bot.add_cog(Helper(bot))
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error(ex)
    finally:
        sys.exit(0)


