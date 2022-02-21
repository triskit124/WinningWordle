from WordleBot import WordleBot


def main():
    """
    Let's play some wordle! This script launches a user game for Wordl with the WordlBot there to give you advice!
    """

    wordleBot = WordleBot(selfPlay=False)
    #wordleBot.SetSolution("wrung")
    wordleBot.play()


if __name__ == "__main__":
    main()
