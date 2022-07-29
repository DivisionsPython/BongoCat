import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Interaction, ButtonStyle, Emoji, PartialEmoji
import os
import aiosqlite
import datetime
import traceback
from rich.console import Console


console = Console()


class Bot(commands.Bot):
    """
    Subclass of `discord.ext.commands.Bot` with automatic extensions loading and database connection.

    Parameters added
    ----------------
    dbconnection: `aiosqlite.Connection`
        The connection to the database.

    dbcursor: `aiosqlite.Cursor`
        The cursor connected to the database.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbconnection = None
        self.dbcursor = None

    async def setup_hook(self):
        for extension in [f.replace('.py', '') for f in os.listdir("listeners") if os.path.isfile(os.path.join("listeners", f))]:
            try:
                await self.load_extension(f"listeners.{extension}")
            except (discord.ClientException, ModuleNotFoundError):
                console.log(
                    f'\u26d4 Failed to load extension: {extension}', style="#ff0000 bold on #ffffff")
        console.log("\u2705 Listeners extensions loaded", style="#00ff00 bold")

        for extension in [f.replace('.py', '') for f in os.listdir("owner") if os.path.isfile(os.path.join("owner", f))]:
            try:
                await self.load_extension(f"owner.{extension}")
            except (discord.ClientException, ModuleNotFoundError):
                console.log(
                    f'\u26d4 Failed to load extension: {extension}', style="#ff0000 bold on #ffffff")
        console.log("\u2705 Owner extensions loaded", style="#00ff00 bold")

        for extension in [f.replace('.py', '') for f in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", f))]:
            try:
                await self.load_extension(f"cogs.{extension}")
            except (discord.ClientException, ModuleNotFoundError):
                console.log(
                    f'\u26d4 Failed to load extension: {extension}', style="#ff0000 bold on #ffffff")
        console.log("\u2705 Cogs extensions loaded", style="#00ff00 bold")

        try:
            self.dbconnection = await aiosqlite.connect('.\databases\database.sqlite')
            self.dbcursor = await self.dbconnection.cursor()
            await self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS economy (
                user_id INTEGER,
                wallet INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0
                )''')
            await self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS welcomer (
                guild_id INTEGER,
                channel_id INTEGER,
                background INTEGER DEFAULT 1
                )''')
            await self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS animals (
                user_id INTEGER,
                bee INTEGER DEFAULT 0,
                bug INTEGER DEFAULT 0,
                snail INTEGER DEFAULT 0,
                rabbit2 INTEGER DEFAULT 0,
                chipmunk INTEGER DEFAULT 0,
                sheep INTEGER DEFAULT 0,
                pig2 INTEGER DEFAULT 0,
                cow2 INTEGER DEFAULT 0,
                deer INTEGER DEFAULT 0,
                owl INTEGER DEFAULT 0,
                boar INTEGER DEFAULT 0,
                frog INTEGER DEFAULT 0,
                wolf INTEGER DEFAULT 0,
                lizard INTEGER DEFAULT 0,
                snake INTEGER DEFAULT 0
                )''')
            await self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS weapons (
                user_id INTEGER,
                axe INTEGER DEFAULT 0,
                knife INTEGER DEFAULT 1,
                staff INTEGER DEFAULT 1,
                sword INTEGER DEFAULT 1,
                dagger INTEGER DEFAULT 0,
                hammer INTEGER DEFAULT 0,
                mace INTEGER DEFAULT 0,
                pickaxe INTEGER DEFAULT 1,
                sickle INTEGER DEFAULT 0
                )''')
            await self.dbconnection.commit()
        except Exception:
            console.log('\u26d4 Error loading database',
                        style="#ff0000 bold on #ffffff")
        else:
            console.log('\u2705 Database loaded', style="#00ff00 bold")

    async def close(self) -> None:
        await self.dbconnection.commit()
        await self.dbcursor.close()
        await self.dbconnection.close()
        console.print('The bot has been turned off',
                      style='#ff0000 bold on #ffffff')
        return await super().close()


class ClassicDetailedEmbed(discord.Embed):
    """
    Subclass of `discord.Embed` with automatic footer and timestamp.

    Parameters added
    ----------------
    user: `discord.User`
        The user needed to create the string "Requested by <user>".
    """

    def __init__(self, user: discord.User, *, colour: discord.Colour = 0xdda7ff, timestamp: datetime.datetime = None):
        if timestamp is None:
            timestamp = datetime.datetime.now()

        super().__init__(colour=colour, timestamp=timestamp)
        self.user = user
        self.set_footer()

    def set_footer(self):
        return super().set_footer(text=f"Requested by {self.user.name}", icon_url=str(self.user.avatar.url))


class ClassicEmbed(discord.Embed):
    """
    Subclass of `discord.Embed` with default `color` parameter (`#dda7ff`).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0xdda7ff))


class SuccessEmbed(discord.Embed):
    """
    Subclass of `discord.Embed` with default `color` parameter (`#00e600`).

    Used to reply to a successful operation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0x00e600))


class WarningEmbed(discord.Embed):
    """
    Subclass of `discord.Embed` with default `color` parameter (`#eed202`).

    Used to reply to a warning/possibly dangerous operation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0xeed202))


class ErrorEmbed(discord.Embed):
    """
    Subclass of `discord.Embed` with default `color` parameter (`#00e600`).

    Used to reply to a failed operation/raised error.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, colour=kwargs.pop("colour", 0xff0000))


class CustomException(Exception):
    """
    Subclass of `Exception` containing an attribute with a `discord.Embed` used to be returned in chat.

    Parameters
    ----------
    error_message: `str`
        The message the exception is raised with, also the `discord.Embed.title` parameter in the embed attribute.

    Attributes added
    ----------------
    errorEmbed: `utils.subclasses.ErrorEmbed | discord.Embed`
        The embed used to be returned in chat.
    """

    def __init__(self, error_message: str = "Unexpected error") -> None:
        super().__init__(error_message)
        self.errorEmbed = ErrorEmbed(
            title=f"\u26d4 {error_message}"
        )


class PrivateView(View):
    """
    Subclass of `discord.ui.View` interactable by only one given user.

    Parameters added
    ----------------
    user: `discord.User`
        The only user who will be able to interact.

    Parameters modified
    -------------------
    timeout: `int`
        Default modified from 180 seconds to 60 seconds, as this view is usually used for user confirmations and doesn't need that much time.
    """

    def __init__(self, user: discord.User, *, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user and interaction.user.id == self.user.id


class ReportButton(Button):
    """
    Subclass of `discord.ui.Button` used to report an unexpected command error with its traceback (Windows terminal `stderr`) to the bot owner's dms.

    Parameters added
    ----------------
    user: `discord.User`
        In the report message, the embed will show the user who reported the error.

    ctx: `discord.ext.commands.Context`
        In the report message, the embed will show the command that raised the error. Also used to catch the traceback.

    error:
        The actual error instance, caught by the error handlers.

    Parameters modified
    -------------------
    style: `discord.ButtonStyle`
        Default modified from `default` to `danger`.

    label: `str`
        The button text. Default set to "Send report".

    emoji: `str | discord.Emoji | discord.PartialEmoji`
        The button emoji. Default set to `incoming_envelope`.
        [Link to emoji](https://emojipedia.org/incoming-envelope/)
    """

    def __init__(self, user: discord.User, ctx: commands.Context, error, *, style: ButtonStyle = ButtonStyle.danger, label: str = "Send report", emoji: Emoji | PartialEmoji | str = "\U0001f4e8"):
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

        owner_appdetails = await interaction.client.application_info()
        owner = interaction.client.get_user(owner_appdetails.owner.id)
        ownerChat = await interaction.client.create_dm(user=owner)

        user = interaction.client.get_user(self.user.id)
        userChat = await interaction.client.create_dm(user=user)

        exception_list = traceback.format_exception(
            type(self.error), self.error, self.error.__traceback__)

        await ownerChat.send(embed=dmEmbed)
        await ownerChat.send(f'''
```
{"".join(exception_list)}
```
''')

        await userChat.send(f"**{self.user.name}** thanks so much for your report, we will check what's wrong as soon as possible :)")

        await interaction.response.edit_message(embed=embed, view=None)

        return await super().callback(interaction)
