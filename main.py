import discord
import logging
import datetime
from discord.ext import commands
from utils.help import MyHelpCommand
from utils.subclasses import Bot
import dotenv
from rich.console import Console
from pyfiglet import figlet_format

intents = discord.Intents.all()
console = Console()

bot = Bot(
    command_prefix=commands.when_mentioned_or(dotenv.dotenv_values('.env')['PREFIX']), intents=intents, case_insensitive=True, help_command=MyHelpCommand())

rightNow = datetime.datetime.now()
rightNow = rightNow.strftime('discord_%d-%m-%Y_started_at_%H-%M-%S')

handler = logging.FileHandler(
    filename=f'./logs/{rightNow}.log', encoding='utf-8', mode='w')

if __name__ == '__main__':
    console.print(
        f"\n{figlet_format('BongoCat', 'standard')}", style='#dda7ff')
    bot.run(dotenv.dotenv_values('.env')[
            'TOKEN'], log_handler=handler, log_level=logging.INFO)
