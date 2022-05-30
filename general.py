import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f'\U0001f4e1 My latency is **{round(self.bot.latency * 1000)}ms**')

    @commands.command()
    async def invite(self, ctx):
        await ctx.channel.send(f"**Invite me**: https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot")
