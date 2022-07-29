import discord
from discord.ext import commands
import random
import requests
from utils.subclasses import ClassicEmbed, ClassicDetailedEmbed, ErrorEmbed, Bot, CustomException


class Gifs(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(description="Kiss a user.")
    async def kiss(self, ctx: commands.Context, member: discord.Member):
        '''Kiss a user.'''
        search_term = "anime kiss"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"Aw come on {ctx.author.name}, I'll give you a kiss \U0001f97a", f"That's sad, {ctx.author.name} :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} kisses {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @commands.command(description="Slap a user.")
    async def slap(self, ctx: commands.Context, member: discord.Member):
        '''Slap a user.'''
        search_term = "anime slap"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"Chill {ctx.author.name}, Don't hurt yourself >:(", f"{ctx.author.name} why :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} slaps {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @commands.command(description="Punch a user.")
    async def punch(self, ctx: commands.Context, member: discord.Member):
        '''Punch a user.'''
        search_term = "anime punch"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"Tf are you doing {ctx.author.name}? Don't! \U0001f624", f"{ctx.author.name} DON'T PUNCH YOURSELF"]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} punches {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @commands.command(description="Hug a user.")
    async def hug(self, ctx: commands.Context, member: discord.Member):
        '''Hug a user.'''
        search_term = "anime hug"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"Do you want a hug {ctx.author.name}? \U0001f97a", f"Aw {ctx.author.name} :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} hugs {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @commands.command(description="Cuddle a user.")
    async def cuddle(self, ctx: commands.Context, member: discord.Member):
        '''Cuddle a user.'''
        search_term = "anime cuddle"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"I'm here for you {ctx.author.name} \U0001f97a", f"Aw {ctx.author.name} :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} cuddles {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @commands.command(aliases=["pat"], description="Headpat a user.")
    async def headpat(self, ctx: commands.Context, member: discord.Member):
        '''Headpat a user'''
        search_term = "anime headpat"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"I'm here for you {ctx.author.name} \U0001f97a", f"Aw {ctx.author.name} :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} headpats {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(Gifs(bot))
