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
            embed = discord.Embed()
            embed.title = "\u26d4 You already have an account!"
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)
        else:
            await add_user(self.bot.connection, ctx.author.id)
            embed = discord.Embed()
            embed.title = f"\u2705 {ctx.author.name}'s account created"
            embed.color = 0x00e600
            await ctx.channel.send(embed=embed)
        await cursor.close()

    @commands.command()
    async def delaccount(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await fetch_user(cursor, ctx.author.id) == ctx.author.id:
            await delete_user(self.bot.connection, ctx.author.id)
            embed = discord.Embed()
            embed.title = f"\u2705 {ctx.author.name}'s account deleted"
            embed.color = 0x00e600
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 You don't have an account!"
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)
        await cursor.close()


async def setup(bot):
    await bot.add_cog(Economy(bot))
