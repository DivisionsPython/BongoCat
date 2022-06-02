import asyncio
import discord
from discord.ext import commands
import requests
import random


class Games(commands.Cog):
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

        await ctx.channel.send(f'The word consists in **{len(randomWord)} letters**.')
        await ctx.channel.send(len(randomWord) * '\u2b1b ')

        try:
            while guess == False and attempts > 0:
                await ctx.channel.send(f'You have **{str(attempts)}** attempts and **10 seconds** to send a letter/word.')
                userGuess = await self.bot.wait_for('message', check=is_correct, timeout=10.0)

        # user inputs a letter
                if len(userGuess.content.lower()) == 1:
                    if not userGuess.content.lower().isalpha():
                        await ctx.channel.send("That's not a letter!")
                    elif userGuess.content.lower() in guessedLetters:
                        await ctx.channel.send('You have already guessed that letter before. Try again!')
                    elif userGuess.content.lower() not in randomWord:
                        await ctx.channel.send('Oops! That letter is not a part of the word.')
                        guessedLetters.append(userGuess.content.lower())
                        attempts -= 1
                    elif userGuess.content.lower() in randomWord:
                        await ctx.channel.send('Awesome! This letter is present in the word!')
                        guessedLetters.append(userGuess.content.lower())
                    else:
                        await ctx.channel.send('Unexpected error. Try again.')

        # user inputs the full word
                elif len(userGuess.content.lower()) == len(randomWord):
                    if userGuess.content.lower() == randomWord:
                        await ctx.channel.send('Awesome! You guessed the word correctly!')
                        guess = True
                    else:
                        await ctx.channel.send("Oops! That's not the word we are looking for.")
                        attempts -= 1

            # user inputs letter and it is not equal to the total
            # number of letters in the word to guess
                else:
                    await ctx.channel.send(
                        'The length of the guess is not the same as the length of the word.')
                    attempts -= 1

                the_status = ''
                if guess == False:
                    for letter in randomWord:
                        if letter in guessedLetters:
                            the_status += letter + " "
                        else:
                            the_status += '\u2b1b '
                    await ctx.channel.send(the_status)

                if the_status == randomWord:
                    await ctx.channel.send('Awesome! You guessed the word correctly!')
                    guess = True
                elif attempts == 0:
                    await ctx.channel.send("Unfortunately, you ran out of guesses.")

        except asyncio.TimeoutError:
            await ctx.channel.send("You ran out of time. Game has ended.")

        except:
            await ctx.channel.send("Unexpected error.")
