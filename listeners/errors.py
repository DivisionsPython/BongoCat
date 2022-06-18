import discord
from discord.ext import commands
import traceback
import sys


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        return await ctx.channel.send(f"""
```
ERROR: {error.__class__.__name__}
DESCRIPTION: {error}
```
        """)


async def setup(bot):
    await bot.add_cog(Errors(bot))
