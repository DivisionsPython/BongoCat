import discord
from discord.ext import commands
import random


class Meters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cool(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed()
            embed.title = f"You are {random.randrange(0, 101)}% cool \U0001f60e"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = f"{member.name} is {random.randrange(0, 101)}% cool \U0001f60e"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def gae(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed()
            embed.title = f"You are {random.randrange(0, 101)}% gae \U0001f308"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = f"{member.name} is {random.randrange(0, 101)}% gae \U0001f308"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def sexy(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed()
            embed.title = f"You are {random.randrange(0, 101)}% sexy \U0001f633"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = f"{member.name} is {random.randrange(0, 101)}% sexy \U0001f633"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def dumb(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed()
            embed.title = f"You are {random.randrange(0, 101)}% dumb \U0001f913"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = f"{member.name} is {random.randrange(0, 101)}% dumb \U0001f913"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def waifu(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed()
            embed.title = f"You are {random.randrange(0, 101)}% a waifu \U0001f61a"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = f"{member.name} is {random.randrange(0, 101)}% a waifu \U0001f61a"
            embed.color = 0xdda7ff
            await ctx.channel.send(embed=embed)
