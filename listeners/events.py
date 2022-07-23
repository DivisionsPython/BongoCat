import discord
from discord.ext import commands
import re
import dotenv
import rich
from rich.console import Console


console = Console()


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"prefix is {dotenv.dotenv_values('.env')['PREFIX']}"), status=discord.Status.idle)
        console.log(
            f'\U0001f4f6 [#00ffff bold]Logged in as [#ffa500 underline]{self.bot.user}[/#ffa500 underline] (Bot ID: [#ffa500 bold]{self.bot.user.id}[/#ffa500 bold])[/#00ffff bold]')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # if self.bot.user in message.mentions:
        #    await message.reply("No bitches? \U0001f610")

        if re.fullmatch(rf"<@!?{self.bot.user.id}>", message.content):
            return await message.channel.send("No bitches? \U0001f610")


async def setup(bot):
    await bot.add_cog(Events(bot))
