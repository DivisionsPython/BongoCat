import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Interaction, ButtonStyle, Emoji, PartialEmoji
import os
import aiosqlite
import datetime
import traceback
import rich
from rich.console import Console


console = Console()


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbconnection = None
        self.dbcursor = None

    async def setup_hook(self):
        for extension in [f.replace('.py', '') for f in os.listdir("listeners") if os.path.isfile(os.path.join("listeners", f))]:
            try:
                await self.load_extension("listeners." + extension)
            except (discord.ClientException, ModuleNotFoundError):
                console.log(
                    f'\u26d4 Failed to load extension: {extension}', style="#ff0000 bold on #ffffff")
        console.log("\u2705 Listeners extensions loaded", style="#00ff00 bold")

        for extension in [f.replace('.py', '') for f in os.listdir("owner") if os.path.isfile(os.path.join("owner", f))]:
            try:
                await self.load_extension("owner." + extension)
            except (discord.ClientException, ModuleNotFoundError):
                console.log(
                    f'\u26d4 Failed to load extension: {extension}', style="#ff0000 bold on #ffffff")
        console.log("\u2705 Owner extensions loaded", style="#00ff00 bold")

        for extension in [f.replace('.py', '') for f in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", f))]:
            try:
                await self.load_extension("cogs." + extension)
            except (discord.ClientException, ModuleNotFoundError):
                console.log(
                    f'\u26d4 Failed to load extension: {extension}', style="#ff0000 bold on #ffffff")
        console.log("\u2705 Cogs extensions loaded", style="#00ff00 bold")

        try:
            self.dbconnection = await aiosqlite.connect('.\databases\database.sqlite')
            self.dbcursor = await self.dbconnection.cursor()
            await self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS eco (
                user_id INTEGER, wallet INTEGER, bank INTEGER
                )''')
            await self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS welcomer (
                guild_id INTEGER, channel_id INTEGER, background INTEGER
                )''')
            await self.dbconnection.commit()
        except:
            console.log('\u26d4 Error loading database',
                        style="#ff0000 bold on #ffffff")
        else:
            console.log('\u2705 Database loaded', style="#00ff00 bold")

    async def close(self) -> None:
        await self.dbconnection.commit()
        await self.dbcursor.close()
        await self.dbconnection.close()
        return await super().close()


class ClassicDetailedEmbed(discord.Embed):
    def __init__(self, user: discord.User, *, colour=0xdda7ff, timestamp=None):
        if timestamp == None:
            timestamp = datetime.datetime.now()

        super().__init__(colour=colour, timestamp=timestamp)
        self.user = user
        self.set_footer()

    def set_footer(self):
        return super().set_footer(text=f"Requested by {self.user.name}", icon_url=str(self.user.avatar.url))


class ClassicEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0xdda7ff))


class SuccessEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0x00e600))


class WarningEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0xeed202))


class ErrorEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0xff0000))


class CustomException(Exception):
    def __init__(self, error_message: str | None = "Unexpected error") -> None:
        super().__init__(error_message)
        self.errorEmbed = ErrorEmbed(
            title=f"\u26d4 {error_message}"
        )


class PrivateView(View):
    def __init__(self, user: discord.User, *, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user and interaction.user.id == self.user.id


class ReportButton(Button):
    def __init__(self, user: discord.User, ctx: commands.Context, error, *, style: ButtonStyle = ButtonStyle.danger, label: str = "Send report", emoji="\U0001f4e8"):
        self.user = user
        self.ctx = ctx
        self.error = error
        super().__init__(style=style, label=label, emoji=emoji)

    async def callback(self, interaction: Interaction):

        embed = SuccessEmbed(
            title="\u2705 Report sent!",
            timestamp=datetime.datetime.now()
        )

        embed.set_footer(
            text=f"Sent by {self.user.name}", icon_url=str(self.user.avatar.url))

        dmEmbed = ErrorEmbed(
            title="\u26d4 Error report"
        )

        dt = datetime.datetime.now()
        formatted = str(dt.strftime('%A %d/%m/%Y, %H:%M:%S'))

        dmEmbed.add_field(
            name=f"Exception in command **`{self.ctx.command}`**", value=formatted)

        dmEmbed.set_footer(
            text=f"Sent by {self.user.name}#{self.user.discriminator}", icon_url=str(self.user.avatar.url))

        owner = interaction.client.get_user(826489186327724095)
        ownerChat = await interaction.client.create_dm(user=owner)

        exception_list = traceback.format_exception(
            type(self.error), self.error, self.error.__traceback__)

        await ownerChat.send(embed=dmEmbed)
        await ownerChat.send(f'''
```
{"".join(exception_list)}
```
''')

        await interaction.response.edit_message(embed=embed, view=None)

        return await super().callback(interaction)
