from utils.config import PREFIX
import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import Button, View
from utils.subclasses import PrivateView
import random
import requests
import json
from utils.economy_functions import add_user, fetch_bank, fetch_wallet, delete_user, update_wallet, update_bank, user_is_known


def getName() -> str:
    url = "https://raw.githubusercontent.com/datasets-io/male-first-names-en/master/lib/dataset.json"
    f = requests.get(url)
    namesList = json.loads(f.text)
    return random.choice(namesList)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["addaccount", "createaccount"])
    async def newaccount(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            embed = discord.Embed()
            embed.title = "\u26d4 You already have an account!"
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)
        else:
            await add_user(self.bot.connection, ctx.author.id)

            embed = discord.Embed()
            embed.title = f"\u2705 {ctx.author.name}'s account created"
            embed.add_field(
                name="Info", value='You have a 0.07% chance of getting a random amount of coins between **0$** and **100$**')
            embed.color = 0x00e600
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command()
    async def delaccount(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            buttonY = Button(label='Confirm', style=ButtonStyle.green)
            buttonN = Button(label='Cancel', style=ButtonStyle.red)
            view = PrivateView(ctx.author)

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

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount: int = None):
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            wallet = await fetch_wallet(cursor, ctx.author.id)
            bank = await fetch_bank(cursor, ctx.author.id)
            if not amount:
                embed = discord.Embed()
                embed.title = '\u26d4 How much money do you want to deposit?'
                embed.color = 0xff0000
                await ctx.channel.send(embed=embed)
            elif wallet < amount:
                embed = discord.Embed()
                embed.title = '\u26d4 Deposit denied'
                if wallet == 0:
                    embed.add_field(
                        name="Reason:", value="Your wallet is empty.")
                else:
                    embed.add_field(
                        name="Reason:", value=f"You can't deposit **{amount}$** in the bank because you only have **{wallet}$** in your wallet.")
                embed.color = 0xff0000
                await ctx.channel.send(embed=embed)
            else:
                await update_wallet(self.bot.connection, ctx.author.id, wallet-amount)
                await update_bank(self.bot.connection, ctx.author.id, bank+amount)
                wallet = await fetch_wallet(cursor, ctx.author.id)
                bank = await fetch_bank(cursor, ctx.author.id)
                embed = discord.Embed()
                embed.title = '\u2705 Deposit successfull'
                embed.add_field(name="Deposit amount:",
                                value=f"{amount}$", inline=False)
                embed.add_field(
                    name="New wallet value:", value=f"{wallet}$", inline=True)
                embed.add_field(
                    name="New bank value:", value=f"{bank}$", inline=True)
                embed.color = 0x00e600
                await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount: int = None):
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            wallet = await fetch_wallet(cursor, ctx.author.id)
            bank = await fetch_bank(cursor, ctx.author.id)
            if not amount:
                embed = discord.Embed()
                embed.title = '\u26d4 How much money do you want to withdraw?'
                embed.color = 0xff0000
                await ctx.channel.send(embed=embed)
            elif bank < amount:
                embed = discord.Embed()
                embed.title = '\u26d4 Withdraw denied'
                if bank == 0:
                    embed.add_field(
                        name="Reason:", value="Your bank is empty.")
                else:
                    embed.add_field(
                        name="Reason:", value=f"You can't withdraw **{amount}$** because you only have **{bank}$** in your bank.")
                embed.color = 0xff0000
                await ctx.channel.send(embed=embed)
            else:
                await update_wallet(self.bot.connection, ctx.author.id, wallet+amount)
                await update_bank(self.bot.connection, ctx.author.id, bank-amount)
                wallet = await fetch_wallet(cursor, ctx.author.id)
                bank = await fetch_bank(cursor, ctx.author.id)
                embed = discord.Embed()
                embed.title = '\u2705 Withdraw successfull'
                embed.add_field(name="Withdraw amount:",
                                value=f"{amount}$", inline=False)
                embed.add_field(
                    name="New wallet value:", value=f"{wallet}$", inline=True)
                embed.add_field(
                    name="New bank value:", value=f"{bank}$", inline=True)
                embed.color = 0x00e600
                await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        cursor = await self.bot.connection.cursor()

        if await user_is_known(cursor, ctx.author.id):
            if await user_is_known(cursor, member.id):
                try:
                    wallet = await fetch_wallet(cursor, member.id)
                    bank = await fetch_bank(cursor, member.id)
                except:
                    embed = discord.Embed()
                    embed.title = "\u26d4 Unexpected error"
                    embed.color = 0xff0000
                    await ctx.channel.send(embed=embed)
                else:
                    embed = discord.Embed()
                    embed.title = f"\U0001f4b8 {member.name}'s balance"
                    embed.add_field(
                        name="Wallet:", value=f"{wallet}$", inline=True)
                    embed.add_field(
                        name="Bank:", value=f"{bank}$", inline=True)
                    embed.color = 0xdda7ff
                    await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed()
                embed.title = "\u26d4 This user hasn't an account yet"
                embed.color = 0xff0000
                await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            if random.random() < 42/100:  # chance of the beg to be successful

                wallet = await fetch_wallet(cursor, ctx.author.id)

                if random.random() < 8/100:  # chance of the beg to give more than 500 coins
                    amount = random.randrange(500, 1001)
                else:  # else less than 500 coins
                    amount = random.randrange(1, 500)

                await update_wallet(self.bot.connection, ctx.author.id, wallet+amount)

                if amount > 500:
                    await ctx.channel.send(f"You got very lucky, {getName()} gave you **{amount}$**")
                else:
                    await ctx.channel.send(f"Good job, {getName()} gave you **{amount}$**")

            else:
                await ctx.channel.send(f"Unfortunately, {getName()} didn't want to give you any money.")

        else:
            embed = discord.Embed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @beg.error
    async def beg_timeout(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed()
            embed.title = "\u26d4 Cooldown"
            embed.add_field(name='Come on bro, chill',
                            value=f"You've already begged recently. Try again in **{round(error.retry_after)}s**")
            embed.color = 0xff0000
            await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, message.author.id):
            if random.random() < 0.07/100:
                wallet = await fetch_wallet(cursor, message.author.id)
                amount = random.randrange(0, 101)
                if amount == 0:
                    await message.channel.send(f"Sadly, {message.author.name} found a wallet on the street but it was empty \U0001f614")
                else:
                    await update_wallet(self.bot.connection, message.author.id, wallet+amount)
                    await message.channel.send(f"{message.author.name}, you got lucky and randomly gained {amount}$ \U0001f604")

        await cursor.close()


async def setup(bot):
    await bot.add_cog(Economy(bot))
