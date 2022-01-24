"""
Implementation of a WordleBot version 1.0
"""

__authors__ = "Tristan Hasseler"
__date__ = "23 Jan 2022"

import random
import string


class WordlBot:

    def __init__(self, selfPlay=False):
        with open('wordledict.txt') as f:
            self.all_words = f.readlines()

        self.selfPlay = selfPlay
        self.numGuesses = 0
        self.gameWon = False
        self.gameLost = False
        self.solution = None
        self.validWords = self.all_words
        self.bestWord = None
        self.wordScores = None
        self.positionalFrequencies = None
        self.normalizedPositionalFrequencies = None
        self.possibleLetters = [list(string.ascii_lowercase) for _ in range(5)]
        self.currentGuess = None
        self.hints = [None, None, None, None, None]

        self.findValidWords()
        self.solution = random.choice(self.validWords)

        # intro sequence
        if not self.selfPlay:
            print(" \n \
                __        __          _       ___          _       __               ____     __\n \
               / /  ___  / /______   | |     / (_)___     | |     / /___  _________/ / /__  / /\n \
              / /  / _ \/ __/ ___/   | | /| / / / __ \    | | /| / / __ \/ ___/ __  / / _ \/ /\n \
             / /__/  __/ /_(__  )    | |/ |/ / / / / /    | |/ |/ / /_/ / /  / /_/ / /  __/_/\n \
            /_____|___/\__/____/     |__/|__/_/_/ /_/     |__/|__/\____/_/   \__,_/_/\___(_)\n")

            print("     Welcome! Let's play some Wordl \n")

    def play(self):
        """
        Main gameplay loop:
            1. find all valid words remaining with hints provided
            2. guess a word
            3. evaluate that guess and provide new hints
        """

        while not self.gameWon and not self.gameLost:
            self.findValidWords()
            self.guess()
            self.evaluateGuess()

        # handle game-over states
        if self.gameWon:
            self.victory()
        elif self.gameLost:
            self.defeat()

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
            elif self.hints[h] == "green":
                guess_str += " \u2714 "
            elif self.hints[h] == "yellow":
                guess_str += " * "
            elif self.hints[h] == "black":
                guess_str += " \u2718 "

        if self.selfPlay:
            # if the WordleBot is playing itself, just generate the best guess and submit it
            self.findMostLikelyWord()
            self.currentGuess = self.bestWord
        else:
            if self.currentGuess is not None:
                print("     Your current hints are: " + self.currentGuess[0] + "  " + self.currentGuess[1] + "  " + self.currentGuess[2] + "  " + self.currentGuess[3] + "  " + self.currentGuess[4] + "\n")
                print("                            " + guess_str + "\n")

            self.findMostLikelyWord() # generate a hint for the human player

            print("     A pretty good guess here would be: " + self.bestWord + "\n")
            print("     Press (a) to view all possibilities remaining\n")
            self.currentGuess = input("     What's your guess? ") # get user guess

            # print out all valid words if requested
            if self.currentGuess == "a":
                print("\n     Valid words remaining are: \n")
                for validWord in self.validWords:
                    print("         -" + validWord + "\n")
                self.currentGuess = input("     What's your guess? ") # get user guess

            print("\n\n")

    def evaluateGuess(self):
        """
        Evaluates a guess against the solution. Will give out hints for each position in the 5-letter word:
            "green" : the letter is in the correct place
            "yellow" : the letter is in the word, but not in this space
            "black" : this letter is not in the word
        This function then prunes out impossible letters out of self.possibleLetters
        """

        # check to see if the solution has been guessed
        if self.currentGuess == self.solution:
            self.gameWon = True
            return

        # look at each letter in guess and compare against solution. Prune possibleLetters accordingly
        for i in range(len(self.solution)):
            if self.currentGuess[i] == self.solution[i]:
                self.hints[i] = "green"
                self.possibleLetters[i] = self.currentGuess[i]
            elif self.currentGuess[i] in self.solution:
                self.hints[i] = "yellow"
                if self.currentGuess[i] in self.possibleLetters[i]:
                    self.possibleLetters[i].remove(self.currentGuess[i])
            else:
                self.hints[i] = "black"
                for j in range(5):
                    if self.currentGuess[i] in self.possibleLetters[j]:
                        self.possibleLetters[j].remove(self.currentGuess[i])

    def victory(self):
        """
        Handles setting the game state to victory
        """
        if not self.selfPlay:
            print("Lets go baby!!! \n")

    def defeat(self):
        """
        Handles setting the game state to defeat
        """
        if not self.selfPlay:
            print(" :( \n")

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
            self.wordScores[word] = score # save result in a Dict

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

    def findValidWords(self):
        """
        Looks through a dictionary of words and weeds out any invalid words according to the current set of possibleLetters
        """

        newValidWords = []
        for word in self.validWords:
            candidate = word.replace('\n', '').lower()  # get rid of newline token and convert to lowercase

            if len(candidate) == 5 and candidate.isalpha():
                if candidate[0] in self.possibleLetters[0] and candidate[1] in self.possibleLetters[1] and candidate[2] in self.possibleLetters[2] and candidate[3] in self.possibleLetters[3] and candidate[4] in self.possibleLetters[4]:
                    newValidWords.append(candidate)

        self.validWords = newValidWords
