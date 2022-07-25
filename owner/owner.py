from discord.ext import commands
import os
import sys
from utils.subclasses import Bot


class Owner(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(hidden=True, description="**`BOT OWNER ONLY`**\n\nUnload an extension (`Cog`).")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, path: str = None, extension: str = None):
        if path == None or extension == None:
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
        if path == None or extension == None:
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
        if path == None or extension == None:
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
        if command == None:
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


async def setup(bot: Bot):
    await bot.add_cog(Owner(bot))
