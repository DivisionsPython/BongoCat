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
ERROR: {error}
```
        """)


def setup(bot):
    bot.add_cog(Errors(bot))
