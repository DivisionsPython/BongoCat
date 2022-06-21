import discord
from discord.ext import commands
import os
import colorama
from colorama import Fore
import aiosqlite

token = "TOKEN"
prefix = ">"
intents = discord.Intents.all()

colorama.init()


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    async def setup_hook(self):
        for extension in [f.replace('.py', '') for f in os.listdir("listeners") if os.path.isfile(os.path.join("listeners", f))]:
            try:
                await self.load_extension("listeners." + extension)
            except (discord.ClientException, ModuleNotFoundError):
                print(Fore.RED + 'Failed to load extension: ' +
                      Fore.YELLOW + extension + Fore.RESET)
        print(Fore.GREEN + "'listeners' extensions loaded." + Fore.RESET)

        for extension in [f.replace('.py', '') for f in os.listdir("owner") if os.path.isfile(os.path.join("owner", f))]:
            try:
                await self.load_extension("owner." + extension)
            except (discord.ClientException, ModuleNotFoundError):
                print(Fore.RED + 'Failed to load extension: ' +
                      Fore.YELLOW + extension + Fore.RESET)
        print(Fore.GREEN + "'owner' extensions loaded." + Fore.RESET)

        for extension in [f.replace('.py', '') for f in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", f))]:
            try:
                await self.load_extension("cogs." + extension)
            except (discord.ClientException, ModuleNotFoundError):
                print(Fore.RED + 'Failed to load extension: ' +
                      Fore.YELLOW + extension + Fore.RESET)
        print(Fore.GREEN + "'cogs' extensions loaded." + Fore.RESET)

        try:
            self.connection = await aiosqlite.connect('.\databases\eco.sqlite')
            cursor = await self.connection.cursor()
            await cursor.execute('''CREATE TABLE IF NOT EXISTS eco (
                user_id INTERGER, wallet INTERGER, bank INTERGER
                )''')
            await self.connection.commit()
            await cursor.close()
        except:
            print(Fore.RED + 'Error loading economy database' + Fore.RESET)
        else:
            print(Fore.GREEN + 'Economy database loaded' + Fore.RESET)


bot = Bot(
    command_prefix=commands.when_mentioned_or(prefix), intents=intents)

bot.run(token)
