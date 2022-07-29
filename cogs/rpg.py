import discord
from discord.ext import commands
from utils.subclasses import Bot, CustomException


class Rpg(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        raise TypeError


async def setup(bot: Bot):
    await bot.add_cog(Rpg(bot))
