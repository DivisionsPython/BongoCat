import discord
from discord.ext import commands
import os
import colorama
from colorama import Fore
import re

token = "TOKEN"
prefix = ">"

colorama.init()


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix))


if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in os.listdir("listeners") if os.path.isfile(os.path.join("listeners", f))]:
        try:
            bot.load_extension("listeners." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(Fore.RED + 'Failed to load extension: ' +
                  Fore.YELLOW + extension + Fore.RESET)

    for extension in [f.replace('.py', '') for f in os.listdir("owner") if os.path.isfile(os.path.join("owner", f))]:
        try:
            bot.load_extension("owner." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(Fore.RED + 'Failed to load extension: ' +
                  Fore.YELLOW + extension + Fore.RESET)

    for extension in [f.replace('.py', '') for f in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", f))]:
        try:
            bot.load_extension("cogs." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(Fore.RED + 'Failed to load extension: ' +
                  Fore.YELLOW + extension + Fore.RESET)


bot.run(token)
