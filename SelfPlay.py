from WordleBot import WordlBot


def main():
    """
    Launches a bunch of self-play games where the WordleBot will have it's own try at beating Wordle.
    This script will be good for benchmarking the WordleBot's performance
    """

    selfPlayIters = 500 # number of games to play
    numGuesses = []

    # play each game
    for i in range(selfPlayIters):
        if i % 100 == 0:
            print("Playing game " + str(i) + "...")

        wordleBot = WordlBot(selfPlay=True)
        wordleBot.play()
        numGuesses.append(wordleBot.numGuesses)

    print("Played " + str(selfPlayIters) + " games. Average guess count was " + str(sum(numGuesses) / len(numGuesses)) + " Best game was " + str(min(numGuesses)) + " guesses. Worst game was " + str(max(numGuesses)))


if __name__ == "__main__":
    main()
