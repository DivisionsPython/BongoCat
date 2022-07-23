import dotenv
import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import Button, View
from utils.subclasses import PrivateView, ClassicEmbed, ClassicDetailedEmbed, SuccessEmbed, WarningEmbed, ErrorEmbed
import random
import requests
import json
from utils.economy_functions import add_user, fetch_bank, fetch_wallet, delete_user, update_wallet, update_bank, user_is_known


PREFIX = dotenv.dotenv_values('.env')['PREFIX']


def getName() -> str:
    url = "https://raw.githubusercontent.com/datasets-io/male-first-names-en/master/lib/dataset.json"
    f = requests.get(url)
    namesList = json.loads(f.text)
    return random.choice(namesList)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["addaccount", "createaccount"], description='Create a new account for our economy system and start playing :)')
    async def newaccount(self, ctx):
        '''Create a new economy account.'''
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            embed = ErrorEmbed()
            embed.title = "\u26d4 You already have an account!"
            await ctx.channel.send(embed=embed)
        else:
            await add_user(self.bot.connection, ctx.author.id)

            embed = SuccessEmbed()
            embed.title = f"\u2705 {ctx.author.name}'s account created"
            embed.add_field(
                name="Info", value='You have a 0.07% chance of getting a random amount of coins between **0$** and **100$**')
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command(description="Delete your economy system account. It's sad to see you go :(")
    async def delaccount(self, ctx):
        '''Delete your economy account.'''
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            buttonY = Button(label='Confirm', style=ButtonStyle.green)
            buttonN = Button(label='Cancel', style=ButtonStyle.red)
            view = PrivateView(ctx.author)

            async def view_timeout():
                embed = ErrorEmbed()
                embed.title = "\u26d4 Time's up. No decision has been taken."
                await embedToEdit.edit(embed=embed, view=None)

            async def conf_callback(interaction):
                await delete_user(self.bot.connection, ctx.author.id)

                embed = SuccessEmbed()
                embed.title = f"\u2705 {ctx.author.name}'s account deleted"

                await interaction.response.edit_message(embed=embed, view=None)

                view.stop()

            async def den_callback(interaction):
                embed = SuccessEmbed()
                embed.title = f"\u2705 Event cancelled"

                await interaction.response.edit_message(embed=embed, view=None)

                view.stop()

            buttonN.callback = den_callback
            buttonY.callback = conf_callback
            view.add_item(buttonY)
            view.add_item(buttonN)

            embed = WarningEmbed()
            embed.title = "\u26a0 Do you really want to delete your account?"
            embed.add_field(name="You still have time!",
                            value="You have **60** seconds to confirm/cancel.")
            embedToEdit = await ctx.channel.send(embed=embed, view=view)

            view.on_timeout = view_timeout
        else:
            embed = ErrorEmbed()
            embed.title = "\u26d4 You don't have an account!"
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command(aliases=["dep"], description="Deposit coins from your wallet to your bank.")
    async def deposit(self, ctx, amount: int = None):
        '''Deposit coins from your wallet to your bank.'''
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            wallet = await fetch_wallet(cursor, ctx.author.id)
            bank = await fetch_bank(cursor, ctx.author.id)
            if amount == None:
                embed = ErrorEmbed()
                embed.title = '\u26d4 How much money do you want to deposit?'
                await ctx.channel.send(embed=embed)
            elif wallet < amount:
                embed = ErrorEmbed()
                embed.title = '\u26d4 Deposit denied'
                if wallet == 0:
                    embed.add_field(
                        name="Reason:", value="Your wallet is empty.")
                else:
                    embed.add_field(
                        name="Reason:", value=f"You can't deposit **{amount}$** in the bank because you only have **{wallet}$** in your wallet.")
                await ctx.channel.send(embed=embed)
            else:
                await update_wallet(self.bot.connection, ctx.author.id, wallet-amount)
                await update_bank(self.bot.connection, ctx.author.id, bank+amount)
                wallet = await fetch_wallet(cursor, ctx.author.id)
                bank = await fetch_bank(cursor, ctx.author.id)
                embed = SuccessEmbed()
                embed.title = '\u2705 Deposit successfull'
                embed.add_field(name="Deposit amount:",
                                value=f"{amount}$", inline=False)
                embed.add_field(
                    name="New wallet value:", value=f"{wallet}$", inline=True)
                embed.add_field(
                    name="New bank value:", value=f"{bank}$", inline=True)
                await ctx.channel.send(embed=embed)
        else:
            embed = ErrorEmbed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command(aliases=["with"], description="Withdraw coins from your bank to your wallet.")
    async def withdraw(self, ctx, amount: int = None):
        '''Withdraw coins from your bank to your wallet.'''
        cursor = await self.bot.connection.cursor()
        if await user_is_known(cursor, ctx.author.id):
            wallet = await fetch_wallet(cursor, ctx.author.id)
            bank = await fetch_bank(cursor, ctx.author.id)
            if amount == None:
                embed = ErrorEmbed()
                embed.title = '\u26d4 How much money do you want to withdraw?'
                await ctx.channel.send(embed=embed)
            elif bank < amount:
                embed = ErrorEmbed()
                embed.title = '\u26d4 Withdraw denied'
                if bank == 0:
                    embed.add_field(
                        name="Reason:", value="Your bank is empty.")
                else:
                    embed.add_field(
                        name="Reason:", value=f"You can't withdraw **{amount}$** because you only have **{bank}$** in your bank.")
                await ctx.channel.send(embed=embed)
            else:
                await update_wallet(self.bot.connection, ctx.author.id, wallet+amount)
                await update_bank(self.bot.connection, ctx.author.id, bank-amount)
                wallet = await fetch_wallet(cursor, ctx.author.id)
                bank = await fetch_bank(cursor, ctx.author.id)
                embed = SuccessEmbed()
                embed.title = '\u2705 Withdraw successfull'
                embed.add_field(name="Withdraw amount:",
                                value=f"{amount}$", inline=False)
                embed.add_field(
                    name="New wallet value:", value=f"{wallet}$", inline=True)
                embed.add_field(
                    name="New bank value:", value=f"{bank}$", inline=True)
                await ctx.channel.send(embed=embed)
        else:
            embed = ErrorEmbed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command(aliases=["bal"], description="Check your (or a user's) balance.")
    async def balance(self, ctx, member: discord.Member = None):
        '''Check your (or a user's) balance.'''
        if not member:
            member = ctx.author

        cursor = await self.bot.connection.cursor()

        if await user_is_known(cursor, ctx.author.id):
            if await user_is_known(cursor, member.id):
                try:
                    wallet = await fetch_wallet(cursor, member.id)
                    bank = await fetch_bank(cursor, member.id)
                except:
                    embed = ErrorEmbed()
                    embed.title = "\u26d4 Unexpected error"
                    await ctx.channel.send(embed=embed)
                else:
                    embed = ClassicDetailedEmbed(user=ctx.author)
                    embed.title = f"\U0001f4b8 {member.name}'s balance"
                    embed.add_field(
                        name="Wallet:", value=f"{wallet}$", inline=True)
                    embed.add_field(
                        name="Bank:", value=f"{bank}$", inline=True)
                    await ctx.channel.send(embed=embed)
            else:
                embed = ErrorEmbed()
                embed.title = "\u26d4 This user hasn't an account yet"
                await ctx.channel.send(embed=embed)
        else:
            embed = ErrorEmbed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @commands.command(description="Really? Don't you have enough money? Imagine begging \U0001f602 You have a chance of getting free coins from someone.")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        '''Have a chance of getting free coins.'''
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
            embed = ErrorEmbed()
            embed.title = "\u26d4 You don't have an account!"
            embed.add_field(name='Create a new account today! \U0001f389',
                            value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
            await ctx.channel.send(embed=embed)

        await cursor.close()

    @beg.error
    async def beg_timeout(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = WarningEmbed()
            embed.title = "\u26a0 Cooldown"
            embed.add_field(name='Come on bro, chill',
                            value=f"You've already begged recently. Try again in **{round(error.retry_after)}s**")
            await ctx.channel.send(embed=embed)

    @commands.command(aliases=["rob"], cooldown_after_parsing=True, description="Oh so you're a real criminal \U0001f977 Try to get some money from someone's bank. Pay attention to don't get caught \U0001f693")
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def bankrob(self, ctx, member: discord.Member):
        """Try stealing coins from someone's bank."""
        error = ErrorEmbed()
        success = SuccessEmbed()
        cursor = await self.bot.connection.cursor()

        if member == ctx.author:
            ctx.command.reset_cooldown(ctx)
            await ctx.channel.send(f"Do you really want to rob yourself? \U0001f602")

        else:
            if await user_is_known(cursor, ctx.author.id):
                if await user_is_known(cursor, member.id):
                    ctxBank = await fetch_bank(cursor, ctx.author.id)
                    memberBank = await fetch_bank(cursor, member.id)
                    if memberBank < 500:
                        error.title = f"\u26d4 {member.name} doesn't have enough money in their bank"
                        error.add_field(
                            name="Details", value=f'The minimum coins required are **500$**, and {member.name} only has **{memberBank}$** in their bank.')
                        ctx.command.reset_cooldown(ctx)
                        await ctx.channel.send(embed=error)
                    elif ctxBank < 500:
                        error.title = "\u26d4 You don't have enough money in your bank"
                        error.add_field(
                            name="Details", value=f'The minimum coins required are **500$**, and you only have **{ctxBank}$** in your bank.')
                        ctx.command.reset_cooldown(ctx)
                        await ctx.channel.send(embed=error)
                    else:
                        if random.random() < 30/100:  # chance of the rob to be successful
                            if memberBank < 2000:  # if the robbed user bank has less than 2000 coins
                                amount = random.randrange(1, (memberBank+1))
                            else:  # else if the robbed user bank has more than 2000 coins
                                if random.random() < 8/100:  # chance of the rob to give more than 2000 coins
                                    amount = random.randrange(
                                        2000, (memberBank+1))
                                else:  # else less than 2000 coins
                                    maxCoins = random.randrange(
                                        memberBank, 2000)
                                    amount = random.randrange(1, maxCoins)

                            await update_bank(self.bot.connection, ctx.author.id, ctxBank+amount)
                            await update_bank(self.bot.connection, member.id, memberBank-amount)

                            if amount >= 2000:
                                success.title = '\U0001f4b8 The robbery was successful and you got very lucky!'
                                success.add_field(
                                    name="You got:", value=f'{amount}$')
                                await ctx.channel.send(embed=success)
                            else:
                                success.title = '\U0001f4b8 The robbery was successful!'
                                success.add_field(
                                    name="You got:", value=f'{amount}$')
                                await ctx.channel.send(embed=success)

                        else:
                            amount = random.randrange(1, 501)
                            await update_bank(self.bot.connection, member.id, memberBank+amount)
                            await update_bank(self.bot.connection, ctx.author.id, ctxBank-amount)
                            await ctx.channel.send(f"Unfortunately, you got caugth by the police \U0001f693 and had to pay **{amount}$** to {member.mention}")

                else:
                    error.title = "\u26d4 This user hasn't an account yet"
                    ctx.command.reset_cooldown(ctx)
                    await ctx.channel.send(embed=error)

            else:
                error.title = "\u26d4 You don't have an account!"
                error.add_field(name='Create a new account today! \U0001f389',
                                value=f'Use the command **`{PREFIX}newaccount`** and start having fun with our economy system :)')
                await ctx.channel.send(embed=error)

            await cursor.close()

    @bankrob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = WarningEmbed()
            embed.title = "\u26a0 Cooldown"
            embed.add_field(name='Come on bro, chill',
                            value=f"You've already robbed recently. Try again in **{round(error.retry_after)}s**")
            await ctx.channel.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = ErrorEmbed()
            embed.title = "\u26d4 Who do you want to rob?"
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
