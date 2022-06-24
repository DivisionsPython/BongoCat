import discord
from discord.ext import commands
import random
from utils.subclasses import ClassicEmbed


class Meters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cool(self, ctx, member: discord.Member = None):
        embed = ClassicEmbed()
        if member is None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% cool \U0001f60e"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% cool \U0001f60e"
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def gae(self, ctx, member: discord.Member = None):
        embed = ClassicEmbed()
        if member is None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% gae \U0001f308"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% gae \U0001f308"
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def sexy(self, ctx, member: discord.Member = None):
        embed = ClassicEmbed()
        if member is None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% sexy \U0001f633"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% sexy \U0001f633"
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def dumb(self, ctx, member: discord.Member = None):
        embed = ClassicEmbed()
        if member is None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% dumb \U0001f913"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% dumb \U0001f913"
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def waifu(self, ctx, member: discord.Member = None):
        embed = ClassicEmbed()
        if member is None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% a waifu \U0001f61a"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% a waifu \U0001f61a"
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def simp(self, ctx, member: discord.Member = None):
        embed = ClassicEmbed()
        if member is None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% a simp \U0001f927"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% a simp \U0001f927"
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def pp(self, ctx, member: discord.Member = None):
        choice = random.randrange(0, 17)
        embed = ClassicEmbed()
        if choice <= 6:
            reply = "Damn that's awkward \U0001f480"
        else:
            reply = "Keep it up king \U0001f60e"
        value = f'8{"=" * choice}D\n{reply}'
        if member is None or member.id == ctx.author.id:
            embed.add_field(name=f"Your pp size \U0001f633", value=value)
            await ctx.channel.send(embed=embed)
        else:
            embed.add_field(
                name=f"{member.name}'s pp size \U0001f633", value=value)
            await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Meters(bot))
