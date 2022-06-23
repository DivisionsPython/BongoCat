import discord
from discord.ext import commands
import datetime
from discord.ui import Button, View
from discord import ButtonStyle
from discord import Spotify


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
        button = Button(
            label='Invite', url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot", style=ButtonStyle.url)
        view = View()
        view.add_item(button)

        embed = discord.Embed()
        embed.title = f"Click the button below to invite me to your server! \U0001f389"
        embed.color = 0xdda7ff
        await ctx.channel.send(embed=embed, view=view)

    @commands.command(aliases=["av", "pfp"])
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        button = Button(
            label='Download avatar', url=str(member.avatar.url), style=ButtonStyle.url)
        view = View()
        view.add_item(button)

        embed = discord.Embed()
        embed.title = f"{member.name}'s avatar"
        embed.set_image(url=str(member.avatar.url))
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar.url))
        embed.timestamp = datetime.datetime.now()
        embed.color = 0xdda7ff
        await ctx.channel.send(embed=embed, view=view)

    @commands.command(aliases=["listening"])
    async def spotify(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        def convert(n) -> str:
            days, seconds = n.days, n.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = (seconds % 60)
            return hours, minutes, seconds

        for activity in member.activities:
            if isinstance(activity, Spotify):
                button = Button(
                    label='Listen on Spotify', url=str(activity.track_url), style=ButtonStyle.url)
                view = View()
                view.add_item(button)

                songLength = convert(activity.duration)

                embed = discord.Embed()
                embed.title = f"{member.name} is listening to"
                embed.add_field(name=activity.title,
                                value=f'by {", ".join(activity.artists)}\nLength: **{songLength[0]}h {songLength[1]}m {songLength[2]}s**')
                embed.set_thumbnail(
                    url="https://raw.githubusercontent.com/madkarmaa/BongoCat/main/utils/spotify_icon.png")
                embed.set_image(url=str(activity.album_cover_url))
                embed.set_footer(
                    text=f"Requested by {ctx.author.name}", icon_url=str(ctx.author.avatar.url))
                embed.timestamp = datetime.datetime.now()
                embed.color = activity.colour
                await ctx.channel.send(embed=embed, view=view)
                break
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 No Spotify activity found"
            embed.add_field(name='Maybe...',
                            value=f"{member.name} might not be listening to Spotify, or maybe the activity is not displayed.")
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
