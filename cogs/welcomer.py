import discord
from discord import ButtonStyle, TextChannel
from discord.ext import commands
from discord.ui import Button, View
from utils.subclasses import PrivateView, ClassicEmbed, ErrorEmbed, SuccessEmbed
from utils.welcomer_functions import delete_welcome_channel, set_welcome_channel, guild_is_known, fetch_channel, update_welcome_channel


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["setwelcome", "welcomer", "welc"])
    async def welcome(self, ctx, channel: discord.TextChannel = None):
        error = ErrorEmbed()
        success = SuccessEmbed()
        if not channel:
            error.title = "\u26d4 No channel provided"
            await ctx.channel.send(embed=error)
        else:
            cursor = await self.bot.connection.cursor()

            if await guild_is_known(cursor, ctx.guild.id):
                error.title = "\u26d4 There's a welcome channel already"
                await ctx.channel.send(embed=error)
            else:
                await set_welcome_channel(self.bot.connection, ctx.guild.id, channel.id)
                success.title = "\u2705 Welcome channel set"
                await ctx.channel.send(embed=success)

            await cursor.close()

    @welcome.error
    async def wrong_channel(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            embed = ErrorEmbed()
            embed.title = "\u26d4 That's not a text channel"
            return await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcomer(bot))
