import discord
from discord import ButtonStyle, TextChannel
from discord.ext import commands
from discord.ui import Button, View
from utils.subclasses import PrivateView
from utils.welcomer_functions import delete_welcome_channel, set_welcome_channel, guild_is_known, fetch_channel, update_welcome_channel


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["setwelcome", "welcomer", "welc"])
    async def welcome(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            await ctx.channel.send("No channel provided")
        else:
            cursor = await self.bot.connection.cursor()

            if await guild_is_known(cursor, ctx.guild.id):
                await ctx.channel.send("There's a welcome channel already")
            else:
                await set_welcome_channel(self.bot.connection, ctx.guild.id, channel.id)
                await ctx.channel.send("Welcome channel set")

            await cursor.close()

    @welcome.error
    async def wrong_channel(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await ctx.channel.send("That's not a text channel")


async def setup(bot):
    await bot.add_cog(Welcomer(bot))
