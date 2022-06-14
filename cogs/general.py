import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed()
        embed.title = f'\U0001f4e1 My latency is **{round(self.bot.latency * 1000)}ms**'
        embed.color = 0xdda7ff
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed()
        embed.title = "Click the link! \U0001f447"
        embed.color = 0xdda7ff
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="»»————-   ★   ————-««",
                        value=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot")
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
