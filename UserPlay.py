from WordleBot import WordlBot


def main():
    """
    Let's play some wordle! This script launches a user game for Wordl with the WordlBot there to give you advice!
    """

    wordleBot = WordlBot(selfPlay=False)
    wordleBot.play()


if __name__ == "__main__":
    main()
