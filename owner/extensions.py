import discord
from discord.ext import commands

# THIS FILE ONLY RELOADS EXTENSIONS FROM './cogs' DIRECTORY, NOT './owner'


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension: str):
        try:
            self.bot.unload_extension(f'cogs.{extension.lower()}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension: str):
        try:
            self.bot.load_extension(f'cogs.{extension.lower()}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        try:
            self.bot.unload_extension(f'cogs.{extension.lower()}')
            self.bot.load_extension(f'cogs.{extension.lower()}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(bot):
    bot.add_cog(Owner(bot))
