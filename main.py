import discord
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


if __name__ == '__main__':
    console.print(figlet_format('BongoCat', 'standard'), style='#dda7ff')
    bot.run(dotenv.dotenv_values('.env')['TOKEN'])
