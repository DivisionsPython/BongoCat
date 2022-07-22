import discord
from discord.ext import commands
import datetime
from discord.ui import Button, View
from discord import ButtonStyle
from discord import Spotify
from utils.subclasses import ClassicDetailedEmbed, ClassicEmbed, ErrorEmbed


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["latency"], description="Check the bot's latency.")
    async def ping(self, ctx):
        '''Check the bot's latency.'''
        embed = ClassicDetailedEmbed(user=ctx.author)
        embed.title = f'\U0001f4e1 My latency is **{round(self.bot.latency * 1000)}ms**'
        await ctx.channel.send(embed=embed)

    @commands.command(description="Invite the bot to your discord server.")
    async def invite(self, ctx):
        '''Invite the bot to your Discord server.'''
        button = Button(
            label='Invite', url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot", style=ButtonStyle.url)
        view = View()
        view.add_item(button)

        embed = ClassicDetailedEmbed(user=ctx.author)
        embed.title = f"Click the button below to invite me to your server! \U0001f389"
        await ctx.channel.send(embed=embed, view=view)

    @commands.command(aliases=["whois"], description="Check a user's profile details. Also download their avatar and banner ;)")
    async def userinfo(self, ctx, member: discord.Member = None):
        '''Check a user's profile details.'''
        if member == None:
            member = ctx.author

        user = ctx.guild.get_member(member.id)

        try:
            bannerUser = await self.bot.fetch_user(member.id)
            banner = str(bannerUser.banner.url)
        except:
            banner = None

        view = View()
        button3 = Button(
            label='User URL', url=f'https://discord.com/users/{user.id}', style=ButtonStyle.url)
        view.add_item(button3)

        button1 = Button(
            label='Download avatar', url=str(user.avatar.url), style=ButtonStyle.url)
        view.add_item(button1)

        if user.display_avatar.url == user.avatar.url:
            pass
        else:
            button4 = Button(
                label='Download server avatar', url=f'{user.display_avatar.url}', style=ButtonStyle.url)
            view.add_item(button4)

        if banner is not None:
            button2 = Button(
                label='Download banner', url=banner, style=ButtonStyle.url)
            view.add_item(button2)
        else:
            pass

        created = user.created_at
        created = datetime.datetime.strftime(created, "%A, %d %B %Y\n%I:%M %p")

        joined = user.joined_at
        joined = datetime.datetime.strftime(joined, "%A, %d %B %Y\n%I:%M %p")

        embed = ClassicDetailedEmbed(user=ctx.author)
        embed.title = f"{user.name}'s user info"
        embed.set_thumbnail(url=str(user.avatar.url))

        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="Discriminator",
                        value=f'#{user.discriminator}', inline=True)
        embed.add_field(name="Bot?", value=user.bot)
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Account created",
                        value=created, inline=True)
        embed.add_field(name="Joined the server", value=joined, inline=True)

        if user.display_name == user.name:
            pass
        else:
            embed.add_field(name="Server nickname",
                            value=user.display_name, inline=True)

        perms = []
        separated_perms = []

        for name, value in user.guild_permissions:
            if value:
                perms.append(name)
            else:
                continue

        if user.id == ctx.guild.owner_id:
            separated_perms = ["Server owner"]
        else:
            for perm in perms:
                separated = perm.split("_")
                reunited_lowercase = " ".join(separated)
                reunited = reunited_lowercase.capitalize()
                separated_perms.append(reunited)

        chars = [x for x in separated_perms]

        if len(chars) > 1024:
            separated_perms = ["Too many to display"]

        embed.add_field(name="Permissions", value=", ".join(
            separated_perms), inline=False)

        roles = [role.mention for role in user.roles[1:]]
        roles.append('@everyone')

        roles_value = " | ".join(roles)
        chars = [x for x in roles_value]

        if len(chars) > 1024:
            roles_value = ["Too many to display"]

        embed.add_field(name="Roles", value=roles_value, inline=False)

        await ctx.channel.send(embed=embed, view=view)

    @commands.command(aliases=["listening"], description="Check a user's Spotify listening activity. This command only checks for the user's Discord activity, this means it won't work if the activity is not displayed.")
    async def spotify(self, ctx, member: discord.Member = None):
        '''Check a user's Spotify listening activity.'''
        if member == None:
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

                embed = ClassicDetailedEmbed(user=ctx.author)
                embed.title = f"{member.name} is listening to"
                embed.add_field(name=activity.title,
                                value=f'by {", ".join(activity.artists)}\nLength: **{songLength[0]}h {songLength[1]}m {songLength[2]}s**')
                embed.set_thumbnail(
                    url="https://raw.githubusercontent.com/madkarmaa/BongoCat/main/utils/img/spotify_icon.png")
                embed.set_image(url=str(activity.album_cover_url))
                await ctx.channel.send(embed=embed, view=view)
                break
        else:
            embed = ErrorEmbed()
            embed.title = "\u26d4 No Spotify activity found"
            embed.add_field(name='Maybe...',
                            value=f"{member.name} might not be listening to Spotify, or maybe the activity is not displayed.")
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def emoji(self, ctx, emoji: discord.PartialEmoji):
        embed = ClassicDetailedEmbed(user=ctx.author)

        button = Button(
            label='Download', url=str(emoji.url), style=ButtonStyle.url)
        view = View()
        view.add_item(button)

        embed.title = "Emoji info"
        embed.set_thumbnail(url=str(emoji.url))
        embed.add_field(name="Name", value=emoji.name, inline=True)
        embed.add_field(name="ID", value=emoji.id, inline=True)
        embed.add_field(name="Animated?", value=emoji.animated, inline=True)

        await ctx.channel.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(General(bot))
