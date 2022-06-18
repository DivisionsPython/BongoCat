import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, path: str = None, extension: str = None):
        if not path or not extension:
            await ctx.channel.send("Which extension do you want to unload?")
        else:
            try:
                await self.bot.unload_extension(
                    f'{path.lower()}.{extension.lower()}')
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.channel.send('**`SUCCESS`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, path: str = None, extension: str = None):
        if not path or not extension:
            await ctx.channel.send("Which extension do you want to load?")
        else:
            try:
                await self.bot.load_extension(f'{path.lower()}.{extension.lower()}')
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.channel.send('**`SUCCESS`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, path: str = None, extension: str = None):
        if not path or not extension:
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


async def setup(bot):
    await bot.add_cog(Owner(bot))
