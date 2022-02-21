"""
Script to determine relative word frequencies for every guessable word in Wordle.
Used to get the Wordle bot to prefer guessing more common words.

Words are ranked by their "commonness" using the wordfreq package, which counts the
number of times a given word appears in a combination of various corpora.

The zipf frequency is used, which weights the commonness of words on a logarithmic scale,
0 being the word does not show up and 8 being the word shows up 1 in 1000 words.

Saves and serializes a Dict to binary as "wordFrequencies.pkl"
"""

from wordfreq import zipf_frequency
import pickle

wordFrequencies = {} # Dict to store word commonness scores

# open the set of valid wordle guesses
with open('wordledict.txt') as f:
    all_words = f.readlines()

# loop through each valid guess and rank the word based on its zipf frequency
for word in all_words:
    word = word.replace('\n', '').lower()
    freq = zipf_frequency(word, 'en', wordlist='large')
    wordFrequencies[word] = freq

# save dict to a binary file
tmp = open("wordFrequencies.pkl", "wb")
pickle.dump(wordFrequencies, tmp)
tmp.close()
