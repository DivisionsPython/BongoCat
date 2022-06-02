import discord
from discord.ext import commands
from errors import Errors
from fun import Fun
from games import Games
from general import General
import colorama
from colorama import Fore
import time
import re

prefix = ">"
colorama.init()

try:
    print(Fore.YELLOW + "Loading token..." + Fore.RESET)
    with open("token.txt", "r") as f:
        content = f.readlines()
        token = content[0]
        f.close()
    print(Fore.GREEN + "Token loaded. Starting bot..." + Fore.RESET)
except FileNotFoundError:
    print(Fore.RED + '"token.txt" file is missing. Creating a new file...' + Fore.RESET)
    newFile = open("token.txt", "x")
    newFile.close()
    print(Fore.GREEN + 'A new "token.txt" file has been created. Please insert the bot token and try again.' + Fore.RESET)
    time.sleep(5)
    exit()
except:
    print(Fore.RED + 'Unexpected error! Check if you have provided the token in "token.txt". If the problem persists, open an issue on GitHub.' + Fore.RESET)
    time.sleep(5)
    exit()


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix), help_command=None)


bot.add_cog(General(bot))
bot.add_cog(Fun(bot))
bot.add_cog(Errors(bot))
bot.add_cog(Games(bot))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"prefix is {prefix}"), status=discord.Status.idle)
    print(Fore.GREEN +
          f'Logged in as {bot.user} (Bot ID: {bot.user.id})' + Fore.RESET)
    print(Fore.YELLOW + "Invite the bot: " + Fore.CYAN +
          f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot" + Fore.RESET)


@bot.event
async def on_message(message: discord.Message) -> None:
    if re.fullmatch(rf"<@!?{bot.user.id}>", message.content):
        await message.channel.send("No bitches? \U0001f610")
        return
    await bot.process_commands(message)


bot.run(token)
