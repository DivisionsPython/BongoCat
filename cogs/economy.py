import discord
from discord.ext import commands
import random
from utils.economy_functions import add_user, fetch_user, fetch_bank, fetch_wallet, delete_user, update_wallet, update_bank


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newaccount(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await fetch_user(cursor, ctx.author.id) == ctx.author.id:
            await ctx.channel.send('You already have an account!')
        else:
            await add_user(self.bot.connection, ctx.author.id)
            await ctx.channel.send(f"{ctx.author.name}'s account added.")
        await cursor.close()


async def setup(bot):
    await bot.add_cog(Economy(bot))
