

def main():
    """
    Finds the best starting word for Wordl according to the following criteria:
        - must be a 5 letter word
        - must contain only english letters

    Words are scored according to how likely each letter is to appear in their respective positions
    """

    # open up a list of english words
    with open('wordledict.txt') as f:
        words = f.readlines()

    validWords = findValidWords(words)
    letterFreqs = findLetterFrequencies(validWords)
    bestWord = findMostLikelyWord(validWords, letterFreqs)

    print(bestWord)


def findMostLikelyWord(words, letterFreqs):
    """
    Finds the word with highest cumulative probability of each letter occurring.
        @param words : list of words to look through
        @param letterFreqs : list of Dictionaries mapping each letter to a normalized frequency
        @return bestCandidate : most likely word!
    """

    wordScores = {}

    # loop through each word in the english language and pick out words of length 5 with no repeating characters
    for word in words:
        score = sum([letterFreqs[i][word[i]] for i in range(len(word))]) # add up frequency scores from each letter
        wordScores[word] = score # save result in a Dict

    # find best candidate, i.e. the key with the largest value associated with it
    bestCandidate = max(wordScores, key=wordScores.get)
    #print(sorted(wordScores.items(), key=lambda x: x[1]))
    return bestCandidate


def findLetterFrequencies(words):
    """
    Takes in a list of words and finds the normalized probability of each letter occurring in each position
        @param words: list of words to look through
        @return normalizedPositionalFrequencies : list of Dictionaries mapping each letter to a normalized frequency
    """

    positionalFrequencies = [{}, {}, {}, {}, {}]
    normalizedPositionalFrequencies = [{}, {}, {}, {}, {}]

    for word in words:
        for i in range(len(word)):
            if word[i] in positionalFrequencies[i].keys():
                positionalFrequencies[i][word[i]] += 1
            else:
                positionalFrequencies[i][word[i]] = 1

    # normalize scores
    for i in range(len(positionalFrequencies)):
        for k in positionalFrequencies[i].keys():
            normalizedPositionalFrequencies[i][k] = positionalFrequencies[i][k] / sum(positionalFrequencies[i].values())

    return normalizedPositionalFrequencies


def findValidWords(words):
    """
    Looks through a dictionary of words and weeds out any invalid words
        @param words : list of words to look through
        @return validWords : list of words that satisfy all rules
    """

    validWords = []
    for word in words:
        candidate = word.replace('\n', '').lower()  # get rid of newline token and convert to lowercase

        if len(candidate) == 5 and candidate.isalpha() and len(set(candidate)) == len(candidate):
            validWords.append(candidate)

    return validWords


if __name__ == "__main__":
    main()
