import discord
from discord.ext import commands
import re
import colorama
from colorama import Fore
from utils.config import PREFIX

colorama.init()


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"prefix is {PREFIX}"), status=discord.Status.idle)
        print(Fore.GREEN +
              f'Logged in as {self.bot.user} (Bot ID: {self.bot.user.id})' + Fore.RESET)
        print(Fore.YELLOW + "Invite the bot: " + Fore.CYAN +
              f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot" + Fore.RESET)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if re.fullmatch(rf"<@!?{self.bot.user.id}>", message.content):
            return await message.channel.send("No bitches? \U0001f610")


async def setup(bot):
    await bot.add_cog(Events(bot))
