import discord
from discord.ext import commands
import random
from utils.subclasses import ClassicEmbed, Bot


class Meters(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(description="How cool are you? Check it out \U0001f60e")
    async def cool(self, ctx: commands.Context, member: discord.Member = None):
        '''How cool?'''
        embed = ClassicEmbed()
        if member == None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% cool \U0001f60e"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% cool \U0001f60e"
            await ctx.channel.send(embed=embed)

    @commands.command(aliases=["howgay", "howgae", "gay"], description="Bro what are you doing with the homies? \U0001f928")
    async def gae(self, ctx: commands.Context, member: discord.Member = None):
        '''How gae?'''
        embed = ClassicEmbed()
        if member == None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% gae \U0001f308"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% gae \U0001f308"
            await ctx.channel.send(embed=embed)

    @commands.command(description="How sexy are you? Please tell us \U0001f60d")
    async def sexy(self, ctx: commands.Context, member: discord.Member = None):
        '''How sexy?'''
        embed = ClassicEmbed()
        if member == None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% sexy \U0001f633"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% sexy \U0001f633"
            await ctx.channel.send(embed=embed)

    @commands.command(description="What's 1 + 1 dude? \U0001f928")
    async def dumb(self, ctx: commands.Context, member: discord.Member = None):
        '''How dumb?'''
        embed = ClassicEmbed()
        if member == None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% dumb \U0001f913"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% dumb \U0001f913"
            await ctx.channel.send(embed=embed)

    @commands.command(description="I've always wanted a waifu, and you? \U0001f60d")
    async def waifu(self, ctx: commands.Context, member: discord.Member = None):
        '''Are you a waifu?'''
        embed = ClassicEmbed()
        if member == None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% a waifu \U0001f61a"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% a waifu \U0001f61a"
            await ctx.channel.send(embed=embed)

    @commands.command(description="Imagine simping. BOZO \U0001f913")
    async def simp(self, ctx: commands.Context, member: discord.Member = None):
        '''Are you a simp?'''
        embed = ClassicEmbed()
        if member == None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% a simp \U0001f927"
            await ctx.channel.send(embed=embed)
        else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% a simp \U0001f927"
            await ctx.channel.send(embed=embed)

    @commands.command(description="How long is your shlong? \U0001f633")
    async def pp(self, ctx: commands.Context, member: discord.Member = None):
        '''How long is your pp?'''
        choice = random.randrange(0, 17)
        embed = ClassicEmbed()
        if choice <= 6:
            reply = "Damn that's awkward \U0001f480"
        else:
            reply = "Keep it up king \U0001f60e"
        value = f'8{"=" * choice}D\n{reply}'
        if member == None or member.id == ctx.author.id:
            embed.add_field(name=f"Your pp size \U0001f633", value=value)
            await ctx.channel.send(embed=embed)
        else:
            embed.add_field(
                name=f"{member.name}'s pp size \U0001f633", value=value)
            await ctx.channel.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(Meters(bot))
