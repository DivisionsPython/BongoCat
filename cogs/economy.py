import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio
from utils.economy_functions import add_user, fetch_user, fetch_bank, fetch_wallet, delete_user, update_wallet, update_bank


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newaccount(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await fetch_user(cursor, ctx.author.id) == ctx.author.id:
            embed = discord.Embed()
            embed.title = "\u26d4 You already have an account!"
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)
        else:
            await add_user(self.bot.connection, ctx.author.id)

            embed = discord.Embed()
            embed.title = f"\u2705 {ctx.author.name}'s account created"
            embed.color = 0x00e600
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command()
    async def delaccount(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await fetch_user(cursor, ctx.author.id) == ctx.author.id:
            buttonY = Button(label='Confirm', style=ButtonStyle.green)
            buttonN = Button(label='Cancel', style=ButtonStyle.red)
            view = View(timeout=60.0)

            async def view_timeout():
                embed = discord.Embed()
                embed.title = "\u26d4 Time's up. No decision has been taken."
                embed.color = 0xff0000
                await embedToEdit.edit(embed=embed, view=None)

            async def conf_callback(interaction):
                await delete_user(self.bot.connection, ctx.author.id)

                embed = discord.Embed()
                embed.title = f"\u2705 {ctx.author.name}'s account deleted"
                embed.color = 0x00e600
                await embedToEdit.edit(embed=embed)

                await interaction.response.edit_message(embed=embed, view=None)

                view.stop()

            async def den_callback(interaction):
                embed = discord.Embed()
                embed.title = f"\u2705 Event cancelled"
                embed.color = 0x00e600
                await embedToEdit.edit(embed=embed)

                await interaction.response.edit_message(embed=embed, view=None)

                view.stop()

            buttonN.callback = den_callback
            buttonY.callback = conf_callback

            # def is_correct(m):
            #    return m.author.id == ctx.author.id

            view.add_item(buttonY)
            view.add_item(buttonN)

            embed = discord.Embed()
            embed.title = "\u26a0 Do you really want to delete your account?"
            embed.add_field(name="You still have time!",
                            value="You have **60** seconds to confirm/cancel.")
            embed.color = 0xeed202
            embedToEdit = await ctx.channel.send(embed=embed, view=view)

            view.on_timeout = view_timeout
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 You don't have an account!"
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)

        await cursor.close()


async def setup(bot):
    await bot.add_cog(Economy(bot))
