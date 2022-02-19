from WordleBot import WordleBot


def main():
    """
    Launches a bunch of self-play games where the WordleBot will have it's own try at beating Wordle.
    This script will be good for benchmarking the WordleBot's performance
    """

    with open('solutions.txt') as f:
        all_words = f.readlines()

    numGuesses = []

    # play each game
    for i, word in enumerate(all_words):

        word = word.replace('\n', '').lower()  # get rid of newline token and convert to lowercase

        if i % 100 == 0:
            print("Playing game " + str(i) + "...")

        wordleBot = WordleBot(selfPlay=True)
        wordleBot.SetSolution(word)
        wordleBot.play()
        numGuesses.append(wordleBot.numGuesses)

    print("Played " + str(len(all_words)) + " games. Average guess count was " + str(sum(numGuesses) / len(numGuesses)) + " Best game was " + str(min(numGuesses)) + " (" + all_words[numGuesses.index(min(numGuesses))].replace('\n', '') + ")" + " guesses. Worst game was " + str(max(numGuesses)) + " (" + all_words[numGuesses.index(max(numGuesses))].replace('\n', '') + ")")


if __name__ == "__main__":
    main()
