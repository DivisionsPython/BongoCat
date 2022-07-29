import discord
from discord.ext import commands
import os
import sys
from utils.subclasses import Bot, CustomException
from utils.economy_functions import user_is_known, update_wallet, update_bank, fetch_wallet, fetch_bank


class Owner(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(hidden=True, description="**`BOT OWNER ONLY`**\n\nUnload an extension (`Cog`).")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, path: str = None, extension: str = None):
        if path is None or extension is None:
            await ctx.channel.send("Which extension do you want to unload?")
        else:
            try:
                await self.bot.unload_extension(
                    f'{path.lower()}.{extension.lower()}')
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.channel.send('**`SUCCESS`**')

    @commands.command(hidden=True, description="**`BOT OWNER ONLY`**\n\nLoad an extension (`Cog`).")
    @commands.is_owner()
    async def load(self, ctx: commands.Context, path: str = None, extension: str = None):
        if path is None or extension is None:
            await ctx.channel.send("Which extension do you want to load?")
        else:
            try:
                await self.bot.load_extension(f'{path.lower()}.{extension.lower()}')
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.channel.send('**`SUCCESS`**')

    @commands.command(hidden=True, description="**`BOT OWNER ONLY`**\n\nReload an extension (`Cog`).")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, path: str = None, extension: str = None):
        if path is None or extension is None:
            await ctx.channel.send("Which extension do you want to reload?")
        else:
            try:
                await self.bot.unload_extension(
                    f'{path.lower()}.{extension.lower()}')
                await self.bot.load_extension(f'{path.lower()}.{extension.lower()}')
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.channel.send('**`SUCCESS`**')

    @commands.command(hidden=True, description="**`BOT OWNER ONLY`**\n\nDisable a command.")
    @commands.is_owner()
    async def disable(self, ctx: commands.Context, command: commands.Command | str = None):
        if command is None:
            await ctx.channel.send("Which command do you want to disable?")
        else:
            try:
                self.bot.remove_command(command)
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            finally:
                await ctx.channel.send('**`SUCCESS`**\nTo add back the command, reload the cog or restart the bot.')

    @commands.command(hidden=True, description="**`BOT OWNER ONLY`**\n\nRestart the bot (`full restart with file edits`).")
    @commands.is_owner()
    async def reboot(self, ctx: commands.Context):
        try:
            await ctx.channel.send('**`RESTARTING...`**')
            os.system('cls')
            os.execl(sys.executable, os.path.abspath("main.py"), *sys.argv)
        except Exception as e:
            await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(hidden=True, description="**`BOT OWNER ONLY`**\n\nTurn off the bot.")
    @commands.is_owner()
    async def stop(self, ctx: commands.Context):
        try:
            await ctx.channel.send('**`TURNING OFF...`**')
            await self.bot.close()
        except Exception as e:
            await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.group(hidden=True, description="**`BOT OWNER ONLY`**\n\nGive a user something in the database.")
    @commands.is_owner()
    async def give(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            raise CustomException("What do you want to do?")

    @give.command()
    async def wallet(self, ctx: commands.Context, amount: int, user: discord.User = None):
        if user is None:
            user = ctx.author

        if not await user_is_known(self.bot.dbcursor, user.id):
            raise CustomException("No account found in the database")

        try:
            wallet = await fetch_wallet(self.bot.dbcursor, user.id)
            await update_wallet(self.bot.dbconnection, self.bot.dbcursor, user.id, wallet+amount)
            await ctx.channel.send(f'**`ADDED {amount}$ TO THE USER WALLET.`**')
        except Exception as e:
            await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @give.command()
    async def bank(self, ctx: commands.Context, amount: int, user: discord.User = None):
        if user is None:
            user = ctx.author

        if not await user_is_known(self.bot.dbcursor, user.id):
            raise CustomException("No account found in the database")

        try:
            bank = await fetch_bank(self.bot.dbcursor, user.id)
            await update_bank(self.bot.dbconnection, self.bot.dbcursor, user.id, bank+amount)
            await ctx.channel.send(f'**`ADDED {amount}$ TO THE USER BANK.`**')
        except Exception as e:
            await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')


async def setup(bot: Bot):
    await bot.add_cog(Owner(bot))
