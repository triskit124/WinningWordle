"""
Implementation of a WordleBot version 1.0
"""

__authors__ = "Tristan Hasseler"
__date__ = "23 Jan 2022"

import random
import math
import string
import pickle


class WordleBot:

    def __init__(self, selfPlay=False, randomGuesses=False, advisorMode=False):

        # load all allowable words
        with open('wordledict.txt') as f:
            self.all_words = f.readlines()

        for w, word in enumerate(self.all_words):
            self.all_words[w] = word.replace('\n', '').lower()

        # load all solution words
        with open('solutions.txt') as f:
            self.solution_words = f.readlines()

        for w, word in enumerate(self.solution_words):
            self.solution_words[w] = word.replace('\n', '').lower()

        # load a dict that maps words to frequencies in the english language
        f = open("wordFrequencies.pkl", "rb")
        self.wordFrequencies = pickle.load(f)
        f.close()

        self.selfPlay = selfPlay
        self.randomGuesses = randomGuesses
        self.advisorMode = advisorMode
        self.numGuesses = 0
        self.gameWon = False
        self.gameLost = False
        self.gameQuit = False
        self.solution = None
        self.validWords = self.all_words
        self.lettersInSolution = set()
        self.bestWord = None
        self.wordScores = None
        self.positionalFrequencies = None
        self.normalizedPositionalFrequencies = None
        self.frequencyWeight = 0.4 # how much to weigh a likely word vs unlikely word when computing score
        self.possibleLetters = [list(string.ascii_lowercase) for _ in range(5)]
        self.currentGuess = None
        self.hints = [None, None, None, None, None]

        self.findValidWords()
        self.previousValidWordsCount = len(self.validWords)

        if not self.advisorMode:
            self.solution = random.choice(self.solution_words)

        # intro sequence
        if not self.selfPlay:
            print(" \n \
                __        __          _       ___          _       __               ____     __\n \
               / /  ___  / /______   | |     / (_)___     | |     / /___  _________/ / /__  / /\n \
              / /  / _ \/ __/ ___/   | | /| / / / __ \    | | /| / / __ \/ ___/ __  / / _ \/ /\n \
             / /__/  __/ /_(__  )    | |/ |/ / / / / /    | |/ |/ / /_/ / /  / /_/ / /  __/_/\n \
            /_____|___/\__/____/     |__/|__/_/_/ /_/     |__/|__/\____/_/   \__,_/_/\___(_)\n")

            print("     Welcome! Let's play some Wordle \n\n")

    def play(self):
        """
        Main gameplay loop:
            1. find all valid words remaining with hints provided
            2. guess a word
            3. evaluate that guess and provide new hints
        """

        while not self.gameWon and not self.gameLost:
            self.guess()

            if self.gameQuit:
                break

            self.evaluateGuess()

        # handle game-over states
        if self.gameWon:
            self.victory()
        elif self.gameLost:
            self.defeat()
        elif self.gameQuit:
            self.quit()

    def guess(self):
        """
        Allows player to enter a guess. If a human is playing, the WordleBot will give its human companion its best
        guess at the solution. If the WordleBot is playing itself, it will go ahead and take its best guess.
        """

        self.numGuesses += 1
        guess_str = ""

        # print out hints given from last turn's guess
        for h in range(len(self.hints)):
            if self.hints[h] is None:
                guess_str += " _ "
            elif self.hints[h] == "g":
                guess_str += " \u2714 "
            elif self.hints[h] == "y":
                guess_str += " * "
            elif self.hints[h] == "b":
                guess_str += " \u2718 "

        if self.selfPlay:
            # if the WordleBot is playing itself, just generate the best guess and submit it
            if self.randomGuesses:
                self.currentGuess = random.choice(self.validWords)
            else:
                self.findMostLikelyWord()
                self.currentGuess = self.bestWord
        else:
            if self.currentGuess is not None:
                print("\n     Your current hints are: " + self.currentGuess[0] + "  " + self.currentGuess[1] + "  " + self.currentGuess[2] + "  " + self.currentGuess[3] + "  " + self.currentGuess[4] + "\n")
                print("                            " + guess_str + "\n")

            self.findMostLikelyWord() # generate a hint for the human player

            print("Guess " + str(self.numGuesses))
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            if self.numGuesses != 1:
                print("     That last guess reduced our valid guesses by %0.2f%% (%0.2f Bits)\n" % (self.findWordsReductionPercentage(), self.findBitsOfInformation()))
            print("     Press (h) to get a hint\n")
            print("     Press (a) to view all " + str(len(self.wordScores.keys())) + " possibilities remaining\n")
            print("     Press (q) to quit\n\n")

            # Ask user to guess and test validity
            while True:
                self.currentGuess = input("     What's your guess? ") # get user guess
                if len(self.currentGuess) == 5 and self.currentGuess.isalpha() and self.currentGuess in self.all_words:
                    break
                elif self.currentGuess == "h":
                    print("\n     I'd recommend guessing: " + self.bestWord + "\n")
                # print out all valid words if requested
                elif self.currentGuess == "a":
                    print("\n     Valid words remaining are: \n")
                    for w in self.wordScores.keys():
                        print("         -%s (confidence: %0.2f)\n" % (w, self.wordScores[w]))
                elif self.currentGuess == "q":
                    self.gameQuit = True
                    break
                else:
                    print("\n     Not a valid guess!\n")
            print("\n\n")

    def evaluateGuess(self):
        """
        Evaluates a guess against the solution. Will give out hints for each position in the 5-letter word:
            "g" : the letter is in the correct place
            "y" : the letter is in the word, but not in this space
            "b" : this letter is not in the word
        This function then prunes out impossible letters out of self.possibleLetters
        """

        if self.advisorMode:
            while True:
                self.hints = input("     Enter the hints given: (g)reen, (y)ellow, (b)lack:  ")
                self.hints = self.hints.lower().replace(" ", "")

                # verify that hints typed are valid
                if len(self.hints) == 5 and self.hints.isalpha() and set(self.hints).issubset(set(["b", "y", "g"])):
                    break
                else:
                    print("\n     Not a valid hint! Examples: gygby, ggggg, bbbbb, ...\n")

            if self.hints == "ggggg":
                self.gameWon = True
                return

            for i in range(len(self.hints)):
                if self.hints[i] == "g":
                    self.lettersInSolution.add(self.currentGuess[i])
                    self.possibleLetters[i] = self.currentGuess[i]
                elif self.hints[i] == "y":
                    self.lettersInSolution.add(self.currentGuess[i])
                    if self.currentGuess[i] in self.possibleLetters[i]:
                        self.possibleLetters[i].remove(self.currentGuess[i])
                else:
                    for j in range(5):
                        if self.currentGuess[i] in self.possibleLetters[j] and len(self.possibleLetters[j]) != 1:
                            self.possibleLetters[j].remove(self.currentGuess[i])
        else:
            # check to see if the solution has been guessed
            if self.currentGuess == self.solution:
                self.gameWon = True
                return

            # look at each letter in guess and compare against solution. Prune possibleLetters accordingly
            for i in range(len(self.solution)):
                if self.currentGuess[i] == self.solution[i]:
                    self.hints[i] = "g"
                    self.lettersInSolution.add(self.currentGuess[i])
                    self.possibleLetters[i] = self.currentGuess[i]
                elif self.currentGuess[i] in self.solution:
                    self.hints[i] = "y"
                    self.lettersInSolution.add(self.currentGuess[i])
                    if self.currentGuess[i] in self.possibleLetters[i]:
                        self.possibleLetters[i].remove(self.currentGuess[i])
                else:
                    self.hints[i] = "b"
                    for j in range(5):
                        if self.currentGuess[i] in self.possibleLetters[j] and len(self.possibleLetters[j]) != 1:
                            self.possibleLetters[j].remove(self.currentGuess[i])

        self.findValidWords()

    def victory(self):
        """
        Handles setting the game state to victory
        """
        if not self.selfPlay:
            print("\n\n     Lets go baby!!! You won in " + str(self.numGuesses) + " guesses! \n")

    def defeat(self):
        """
        Handles setting the game state to defeat
        """
        if not self.selfPlay:
            print("\n\n:-(")

    def quit(self):
        """
        Handles quitting the game early
        """
        if not self.selfPlay:
            print("     See You next time!\n")

    def findMostLikelyWord(self):
        """
        Finds the word with the highest cumulative probability of each letter occurring. Used to select the best guess given
        the current set of validWords.
        """

        self.wordScores = {}
        self.findLetterFrequencies() # look through remaining dictionary and count occurrences of letters in each position

        # loop through each word in the english language and pick out words of length 5 with no repeating characters
        for word in self.validWords:
            score = sum([self.normalizedPositionalFrequencies[i][word[i]] for i in range(len(word))]) # add up frequency scores from each letter
            score += self.frequencyWeight * self.wordFrequencies[word] # add score based on how common the word is
            self.wordScores[word] = score # save result in a Dict

        self.wordScores = dict(sorted(self.wordScores.items(), key=lambda item: item[1], reverse=True)) # sort by value

        # find the best candidate, i.e. the key with the largest value associated with it
        self.bestWord = max(self.wordScores, key=self.wordScores.get)

    def findLetterFrequencies(self):
        """
        Takes in a list of words and finds the normalized probability of each letter occurring in each position. Functions
        mostly as a helper function for self.findMostLikelyWord()
        """

        self.positionalFrequencies = [{}, {}, {}, {}, {}]
        self.normalizedPositionalFrequencies = [{}, {}, {}, {}, {}]

        for word in self.validWords:
            for i in range(len(word)):
                if word[i] in self.positionalFrequencies[i].keys():
                    self.positionalFrequencies[i][word[i]] += 1
                else:
                    self.positionalFrequencies[i][word[i]] = 1

        # normalize scores
        for i in range(len(self.positionalFrequencies)):
            for k in self.positionalFrequencies[i].keys():
                self.normalizedPositionalFrequencies[i][k] = self.positionalFrequencies[i][k] / sum(self.positionalFrequencies[i].values())

    def SetSolution(self, solution):
        self.solution = solution
    
    def findValidWords(self):
        """
        Looks through a dictionary of words and weeds out any invalid words according to the current set of possibleLetters
        """

        newValidWords = []
        self.previousValidWordsCount = len(self.validWords)
        for word in self.validWords:
            candidate = word.replace('\n', '').lower()  # get rid of newline token and convert to lowercase

            if len(candidate) == 5 and candidate.isalpha():
                if candidate[0] in self.possibleLetters[0] and candidate[1] in self.possibleLetters[1] and candidate[2] in self.possibleLetters[2] and candidate[3] in self.possibleLetters[3] and candidate[4] in self.possibleLetters[4]:
                    if set(self.lettersInSolution).issubset(set(candidate)):
                        newValidWords.append(candidate)

        self.validWords = newValidWords

    def findWordsReductionPercentage(self):
        """
        Function to determine the percent reduction of the valid words space by the previous guess
        """
        return 100 * (1 - len(self.validWords) / self.previousValidWordsCount)

    def findBitsOfInformation(self):
        """
        Helper function to calculate the number of bits of information gained by a guess.
        Information is calculated as: H = -log2(p(x))
        """
        return -math.log2(len(self.validWords) / self.previousValidWordsCount)



