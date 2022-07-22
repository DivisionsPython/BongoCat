import discord
from discord.ext import commands
from utils.config import TOKEN, PREFIX
from utils.help import MyHelpCommand
from utils.subclasses import Bot

intents = discord.Intents.all()

bot = Bot(
    command_prefix=commands.when_mentioned_or(PREFIX), intents=intents, case_insensitive=True, help_command=MyHelpCommand())


bot.run(TOKEN)
