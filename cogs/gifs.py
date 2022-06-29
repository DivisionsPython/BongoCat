import discord
from discord.ext import commands
import random
import requests
from utils.subclasses import ClassicEmbed, ClassicDetailedEmbed, ErrorEmbed


class Gifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Kiss a user.")
    async def kiss(self, ctx, member: discord.Member):
        '''Kiss a user.'''
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
            embed = ErrorEmbed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} kisses {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @kiss.error
    async def kiss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = "Who you wanna kiss?"
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

    @commands.command(description="Slap a user.")
    async def slap(self, ctx, member: discord.Member):
        '''Slap a user.'''
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
            embed = ErrorEmbed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} slaps {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = "Who you wanna slap?"
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

    @commands.command(description="Punch a user.")
    async def punch(self, ctx, member: discord.Member):
        '''Punch a user.'''
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
            embed = ErrorEmbed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} punches {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @punch.error
    async def punch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = "Who you wanna punch?"
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

    @commands.command(description="Hug a user.")
    async def hug(self, ctx, member: discord.Member):
        '''Hug a user.'''
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
            embed = ErrorEmbed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} hugs {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = "Who you wanna hug?"
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

    @commands.command(description="Cuddle a user.")
    async def cuddle(self, ctx, member: discord.Member):
        '''Cuddle a user.'''
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
            embed = ErrorEmbed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} cuddles {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @cuddle.error
    async def cuddle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = "Who you wanna cuddle?"
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)

    @commands.command(aliases=["pat"], description="Headpat a user.")
    async def headpat(self, ctx, member: discord.Member):
        '''Headpat a user'''
        search_term = "anime headpat"
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
            embed = ErrorEmbed()
            embed.title = "\u26d4 Error connecting to the Tenor API"
            return await ctx.channel.send(embed=embed)

        if member == ctx.author:
            await ctx.channel.send(random.choice(sadReplyList))
        else:
            embed = ClassicEmbed()
            embed.title = f"{ctx.author.name} headpats {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.channel.send(embed=embed)

    @headpat.error
    async def headpat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = "Who you wanna headpat?"
            return await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            embed = ErrorEmbed()
            embed.title = f'\u26d4 {error}'
            return await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gifs(bot))
