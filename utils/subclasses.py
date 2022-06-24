import discord
from discord.ext import commands
from discord.ui import Button, View
import colorama
from colorama import Fore
import os
import aiosqlite
import datetime


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        colorama.init()

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
            self.connection = await aiosqlite.connect('.\databases\database.sqlite')
            cursor = await self.connection.cursor()
            await cursor.execute('''CREATE TABLE IF NOT EXISTS eco (
                user_id INTERGER, wallet INTERGER, bank INTERGER
                )''')
            await cursor.execute('''CREATE TABLE IF NOT EXISTS welcomer (
                guild_id INTERGER, channel_id INTERGER, background INTERGER
                )''')
            await self.connection.commit()
            await cursor.close()
        except:
            print(Fore.RED + 'Error loading database' + Fore.RESET)
        else:
            print(Fore.GREEN + 'Database loaded' + Fore.RESET)


class PrivateView(discord.ui.View):
    def __init__(self, user: discord.User, *, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user and interaction.user.id == self.user.id


class ClassicEmbed(discord.Embed):
    def __init__(self, *, colour=0xdda7ff):
        super().__init__(colour=colour)


class ClassicDetailedEmbed(discord.Embed):
    def __init__(self, user: discord.User, *, colour=0xdda7ff, timestamp=None):
        if timestamp == None:
            timestamp = datetime.datetime.now()

        super().__init__(colour=colour, timestamp=timestamp)
        self.user = user
        self.set_footer()

    def set_footer(self):
        return super().set_footer(text=f"Requested by {self.user.name}", icon_url=str(self.user.avatar.url))


class SuccessEmbed(discord.Embed):
    def __init__(self, *, colour=0x00e600):
        super().__init__(colour=colour)


class WarningEmbed(discord.Embed):
    def __init__(self, *, colour=0xeed202):
        super().__init__(colour=colour)


class ErrorEmbed(discord.Embed):
    def __init__(self, *, colour=0xff0000):
        super().__init__(colour=colour)


class ErrorReportEmbed(discord.Embed):
    def __init__(self, user: discord.User, *, colour=0xff0000, timestamp=None):
        if timestamp == None:
            timestamp = datetime.datetime.now()

        super().__init__(colour=colour, timestamp=timestamp)
        self.user = user
        self.set_footer()

    def set_footer(self):
        return super().set_footer(text=f"Sent by {self.user.name}", icon_url=str(self.user.avatar.url))
