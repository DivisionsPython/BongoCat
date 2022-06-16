import discord
from discord.ext import commands
import random
import sqlite3
import colorama
from colorama import Fore

colorama.init()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            db = sqlite3.connect('.\databases\eco.sqlite')
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS eco (
                user_id INTERGER, wallet INTERGER, bank INTERGER
                )''')
            print(Fore.GREEN + 'Economy files loaded' + Fore.RESET)
        except:
            print(Fore.RED + 'Error loading the economy database' + Fore.RESET)


def setup(bot):
    bot.add_cog(Economy(bot))
