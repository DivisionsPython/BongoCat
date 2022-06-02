import random
import requests


def getWord():
    url = "https://raw.githubusercontent.com/meetDeveloper/freeDictionaryAPI/master/meta/wordList/english.txt"
    f = requests.get(url)
    words = f.text.splitlines()
    return random.choice(words).lower()


randomWord = getWord()
guessedLetters = []
attempts = 6
guess = False

print('The word consists in', len(randomWord), 'letters.')
print(len(randomWord) * '_ ')

while guess == False and attempts > 0:
    print('You have ' + str(attempts) + ' attempts')
    userGuess = input(
        'Guess a letter in the word or enter the full word: ').lower()
    # user inputs a letter
    if len(userGuess) == 1:
        if not userGuess.isalpha():
            print("That's not a letter!")
        elif userGuess in guessedLetters:
            print('You have already guessed that letter before. Try again!')
        elif userGuess not in randomWord:
            print('Oops! That letter is not a part of the word.')
            guessedLetters.append(userGuess)
            attempts -= 1
        elif userGuess in randomWord:
            print('Awesome! This letter is present in the word!')
            guessedLetters.append(userGuess)
        else:
            print('Unexpected error. Try again.')

    # user inputs the full word
    elif len(userGuess) == len(randomWord):
        if userGuess == randomWord:
            print('Awesome! You guessed the word correctly!')
            guess = True
        else:
            print('Oops! that was not the word we were looking for.')
            attempts -= 1

        # user inputs letter and it is not equal to the total
        # number of letters in the word to guess
    else:
        print('The length of the guess is not the same as the length of the word.')
        attempts -= 1

    the_status = ''
    if guess == False:
        for letter in randomWord:
            if letter in guessedLetters:
                the_status += letter + " "
            else:
                the_status += '_ '
        print(the_status)

    if the_status == randomWord:
        print('Awesome! You guessed the word correctly!')
        guess = True
    elif attempts == 0:
        print("Unfortunately you ran out of guesses.")
