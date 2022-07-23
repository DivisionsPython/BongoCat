import discord
from discord.ext import commands
from utils.help import MyHelpCommand
from utils.subclasses import Bot
import dotenv

intents = discord.Intents.all()

bot = Bot(
    command_prefix=commands.when_mentioned_or(dotenv.dotenv_values('.env')['PREFIX']), intents=intents, case_insensitive=True, help_command=MyHelpCommand())


bot.run(dotenv.dotenv_values('.env')['TOKEN'])
