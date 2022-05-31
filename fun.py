import discord
from discord.ext import commands
import random
import requests
import json


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        search_term = "anime kiss"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        gif_list = []
        sadReplyList = [
            f"Aw come on {ctx.author.name}, I'll give you a kiss \U0001f97a", f"That's sad, {ctx.author.name} :("]

        if r.status_code == 200:
            data = r.json()
            for details in data["results"]:
                for media in details["media"]:
                    gif_list.append(media["gif"]["url"])
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed()
            embed.title = f"{ctx.author.name} kisses {member.name}"
            embed.color = 0xdda7ff
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed()
            embed.title = "Who you wanna kiss?"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        search_term = "anime slap"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        gif_list = []
        sadReplyList = [
            f"Chill {ctx.author.name}, Don't hurt yourself >:(", f"{ctx.author.name} why :("]

        if r.status_code == 200:
            data = r.json()
            for details in data["results"]:
                for media in details["media"]:
                    gif_list.append(media["gif"]["url"])
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed()
            embed.title = f"{ctx.author.name} slaps {member.name}"
            embed.color = 0xdda7ff
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed()
            embed.title = "Who you wanna slap?"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

    @commands.command()
    async def punch(self, ctx, member: discord.Member):
        search_term = "anime punch"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        gif_list = []
        sadReplyList = [
            f"Tf are you doing {ctx.author.name}? Don't! \U0001f624", f"{ctx.author.name} DON'T PUNCH YOURSELF"]

        if r.status_code == 200:
            data = r.json()
            for details in data["results"]:
                for media in details["media"]:
                    gif_list.append(media["gif"]["url"])
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed()
            embed.title = f"{ctx.author.name} punches {member.name}"
            embed.color = 0xdda7ff
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @punch.error
    async def punch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed()
            embed.title = "Who you wanna punch?"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        search_term = "anime hug"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        gif_list = []
        sadReplyList = [
            f"Do you want a hug {ctx.author.name}? \U0001f97a", f"Aw {ctx.author.name} :("]

        if r.status_code == 200:
            data = r.json()
            for details in data["results"]:
                for media in details["media"]:
                    gif_list.append(media["gif"]["url"])
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed()
            embed.title = f"{ctx.author.name} hugs {member.name}"
            embed.color = 0xdda7ff
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed()
            embed.title = "Who you wanna hug?"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

    @commands.command()
    async def cuddle(self, ctx, member: discord.Member):
        search_term = "anime cuddle"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        gif_list = []
        sadReplyList = [
            f"I'm here for you {ctx.author.name} \U0001f97a", f"Aw {ctx.author.name} :("]

        if r.status_code == 200:
            data = r.json()
            for details in data["results"]:
                for media in details["media"]:
                    gif_list.append(media["gif"]["url"])
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed()
            embed.title = f"{ctx.author.name} cuddles {member.name}"
            embed.color = 0xdda7ff
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @cuddle.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed()
            embed.title = "Who you wanna cuddle?"
            embed.color = 0xff0000
            return await ctx.channel.send(embed=embed)
