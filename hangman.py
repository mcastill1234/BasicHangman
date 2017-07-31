# Problem Set 2, hangman.py
# Name: Mario Castillo
# Collaborators: None
# Time spent: started 07/21/2017 - 07/26/2017

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for char in secret_word:
        if char in letters_guessed:
            continue
        else:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    guess_sofar = ''
    for char in secret_word:
        if char in letters_guessed:
            guess_sofar += ' ' + char
        else:
            guess_sofar += ' _ '  # I prefer to use ' _ ' instead of '_ '. Looks better at print
    return guess_sofar


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    import string

    availletters = ''
    for char in string.ascii_lowercase:
        if char in letters_guessed:
            continue
        else:
            availletters += char
    return availletters
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    #secret_word = 'mario'
    print("Welcome to the game Hangman! \n I am thinking of a word that is",
            len(secret_word), "letters long. \n--------------------")

    # Initialize numer of guesses left, letters guessed vector and warnings
    guesses = 6
    letters_guessed = []
    warnings = 3

    # Game loop until guesses are over
    while guesses > 0:
        while warnings > 0:

            print('You have {} guesses left.'.format(guesses))  # using {} and .format to print
            print('Available letteres:', get_available_letters(letters_guessed))
            letter = str(input('Please enter a letter: '))
            if not str.isalpha(letter):
                warnings -= 1
                print('Opps! That is not a valid letter. You have {} warnings left:'
                      .format(warnings), get_guessed_word(secret_word, letters_guessed),
                      '\n-------------------------')
            elif letter in letters_guessed:
                warnings -= 1
                print('Opps! You already guessed that letter. You have {} warnings left: \n'
                      .format(warnings), get_guessed_word(secret_word, letters_guessed),
                      '\n-------------------------')
            else:  # if its a letter and has not been guessed already, then:
                letter = str.lower(letter)  # lower case it
                letters_guessed += letter   # add to letters guessed vector
                if letter in secret_word:
                    print('Good guess:', get_guessed_word(secret_word, letters_guessed), '\n'
                         '---------------------')
                    if is_word_guessed(secret_word, letters_guessed):
                        print('Contratulations, you won!')
                        print('Your total score for this game is: ', guesses*len(letters_guessed))
                        return 0
                else:
                    if letter in ['a','e','i','o','u']:
                        guesses -= 2
                    else:
                        guesses -= 1
                    print('Opps! That letter is not in my word:', get_guessed_word(secret_word,
                        letters_guessed), '\n-------------------------')
                    if guesses <= 0:
                        print('You lost. The word was: ', secret_word)
                        return 0
        warnings = 3
        guesses -= 1
        print('Oops! you ran out of warnings, you loose one guess')
    print('You lost. The word was: ', secret_word)
    return 0



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''

    temp = my_word.replace(" ", "")

    if len(temp) != len(other_word):
        return False
    for i in range(len(other_word)):
        if temp[i] == '_':
            if other_word[i] in temp:
                return False
        elif temp[i] != other_word[i]:
            return False

    return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = ''

    for cword in wordlist:
        if match_with_gaps(my_word, cword):
            matches += cword + ' '
    if matches == '':
        print('No matches found')
    else:
        print(matches)
    return 0

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    # secret_word = 'mario'
    print("Welcome to the game Hangman! \n I am thinking of a word that is",
          len(secret_word), "letters long. \n--------------------")

    # Initialize numer of guesses left, letters guessed vector and warnings
    guesses = 6
    letters_guessed = []
    warnings = 3

    # Game loop until guesses are over
    while guesses > 0:
        while warnings > 0:

            print('You have {} guesses left.'.format(guesses))
            print('Available letteres:', get_available_letters(letters_guessed))
            letter = str(input('Please enter a letter: '))
            if not str.isalpha(letter):
                if letter == '*':
                    show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                    continue
                warnings -= 1
                print('Opps! That is not a valid letter. You have {} warnings left:'
                      .format(warnings), get_guessed_word(secret_word, letters_guessed),
                      '\n-------------------------')
            elif letter in letters_guessed:
                warnings -= 1
                print('Opps! You already guessed that letter. You have {} warnings left: \n'
                      .format(warnings), get_guessed_word(secret_word, letters_guessed),
                      '\n-------------------------')
            else:
                letter = str.lower(letter)
                letters_guessed += letter
                if letter in secret_word:
                    print('Good guess:', get_guessed_word(secret_word, letters_guessed), '\n'
                                                                                         '---------------------')
                    if is_word_guessed(secret_word, letters_guessed):
                        print('Contratulations, you won!')
                        print('Your total score for this game is: ', guesses * len(letters_guessed))
                        return 0
                else:
                    if letter in ['a', 'e', 'i', 'o', 'u']:
                        guesses -= 2
                    else:
                        guesses -= 1
                    print('Opps! That letter is not in my word:', get_guessed_word(secret_word,
                                                                                   letters_guessed),
                          '\n-------------------------')
                    if guesses <= 0:
                        print('You lost. The word was: ', secret_word)
                        return 0
        warnings = 3
        guesses -= 1
        print('Oops! you ran out of warnings, you loose one guess')
    print('You lost. The word was: ', secret_word)
    return 0



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
