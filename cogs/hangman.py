import asyncio
import discord
from discord.ext import commands
import requests
import random


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hangman(self, ctx):

        def getWord():
            url = "https://raw.githubusercontent.com/meetDeveloper/freeDictionaryAPI/master/meta/wordList/english.txt"
            f = requests.get(url)
            words = f.text.splitlines()
            return random.choice(words).lower()

        def is_correct(m):
            return m.author.id == ctx.author.id

        randomWord = getWord()
        guessedLetters = []
        attempts = 10
        guess = False
        the_status = len(randomWord) * '\u2b1b'

        embed = discord.Embed()
        embed.title = f'\u2753 The word consists in **{len(randomWord)} letters**.'
        embed.color = 0xdda7ff
        embed.add_field(
            name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
        embed.add_field(name="Word status", value=str(
            the_status), inline=False)
        embedToEdit = await ctx.channel.send(embed=embed)

        try:
            while guess == False and attempts > 0:
                userGuess = await self.bot.wait_for('message', check=is_correct, timeout=10.0)

        # user inputs a letter
                if len(userGuess.content) == 1:

                    for i in range(len(randomWord)):
                        if userGuess.content.lower() == randomWord[i]:
                            the_status = the_status[:i] + \
                                userGuess.content.lower() + the_status[i+1:]

                    if not userGuess.content.lower().isalpha():
                        embed = discord.Embed()
                        embed.title = "\u26d4 That's not a letter!"
                        embed.color = 0xff0000
                        embed.add_field(
                            name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
                        embed.add_field(name="Word status", value=str(
                            the_status), inline=False)
                        await embedToEdit.edit(embed=embed)

                    elif userGuess.content.lower() in guessedLetters:
                        embed = discord.Embed()
                        embed.title = "\u26d4 You already have guessed that letter before, try again."
                        embed.color = 0xff0000
                        embed.add_field(
                            name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
                        embed.add_field(name="Word status", value=str(
                            the_status), inline=False)
                        await embedToEdit.edit(embed=embed)

                    elif userGuess.content.lower() not in randomWord:
                        embed = discord.Embed()
                        embed.title = "\u26d4 That letter is not present in the word!"
                        embed.color = 0xff0000

                        attempts -= 1

                        embed.add_field(
                            name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
                        embed.add_field(name="Word status", value=str(
                            the_status), inline=False)

                        guessedLetters.append(userGuess.content.lower())

                        await embedToEdit.edit(embed=embed)

                    elif userGuess.content.lower() in randomWord:
                        embed = discord.Embed()
                        embed.title = "\u2705 Awesome, that letter is present in the word!"
                        embed.color = 0x00e600
                        embed.add_field(
                            name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
                        embed.add_field(name="Word status", value=str(
                            the_status), inline=False)

                        guessedLetters.append(userGuess.content.lower())

                        await embedToEdit.edit(embed=embed)

                    else:
                        embed = discord.Embed()
                        embed.title = "\u26d4 Unexpected error, try again."
                        embed.color = 0xff0000
                        embed.add_field(
                            name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
                        embed.add_field(name="Word status", value=str(
                            the_status), inline=False)
                        await embedToEdit.edit(embed=embed)

        # user inputs the full word
                elif len(userGuess.content.lower()) == len(randomWord):
                    if userGuess.content.lower() == randomWord:
                        embed = discord.Embed()
                        embed.title = "\U0001f3c5 Perfect, you've guessed the word!"
                        embed.color = 0x00e600

                        guess = True

                        await embedToEdit.edit(embed=embed)

                    else:
                        embed = discord.Embed()
                        embed.title = "\u26d4 That's not the word we are looking for, try again."
                        embed.color = 0xff0000

                        attempts -= 1

                        embed.add_field(
                            name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
                        embed.add_field(name="Word status", value=str(
                            the_status), inline=False)

                        await embedToEdit.edit(embed=embed)

            # user inputs letter and it is not equal to the total
            # number of letters in the word to guess
                else:
                    embed = discord.Embed()
                    embed.title = "\u26d4 The word you've guessed hasn't the same length of the one we're searching, try again."
                    embed.color = 0xff0000

                    attempts -= 1

                    embed.add_field(
                        name="Player status", value=f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.', inline=False)
                    embed.add_field(name="Word status", value=str(
                        the_status), inline=False)

                    await embedToEdit.edit(embed=embed)

                if the_status == randomWord:
                    embed = discord.Embed()
                    embed.title = "\U0001f3c5 Perfect, you've guessed the word!"
                    embed.color = 0x00e600
                    await embedToEdit.edit(embed=embed)
                    guess = True

                elif attempts == 0:
                    embed = discord.Embed()
                    embed.title = "\U0001f615 Unfortunately, you ran out of guesses."
                    embed.color = 0xff0000
                    await embedToEdit.edit(embed=embed)

        except asyncio.TimeoutError:
            embed = discord.Embed()
            embed.title = "\u26d4 Time's up. Game has ended."
            embed.color = 0xff0000
            await embedToEdit.edit(embed=embed)

        except:
            embed = discord.Embed()
            embed.title = "\u26d4 Unexpected error."
            embed.color = 0xff0000
            await embedToEdit.edit(embed=embed)


def setup(bot):
    bot.add_cog(Hangman(bot))
