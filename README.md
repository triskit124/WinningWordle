        __        __          _       ___          _       __               ____     __ 
       / /  ___  / /______   | |     / (_)___     | |     / /___  _________/ / /__  / /
      / /  / _ \/ __/ ___/   | | /| / / / __ \    | | /| / / __ \/ ___/ __  / / _ \/ /
     / /__/  __/ /_(__  )    | |/ |/ / / / / /    | |/ |/ / /_/ / /  / /_/ / /  __/_/ 
    /_____|___/\__/____/     |__/|__/_/_/ /_/     |__/|__/\____/_/   \__,_/_/\___(_))

# WordleBot
Helps humans play the game, [Wordle](https://www.powerlanguage.co.uk/wordle/)

The rules are simple:
<ol>
  <li>The word must have 5 only letters</li>
  <li>The word must be a real, valid word</li>
</ol>

Words are ranked by WordlBot based on how likely each of their letters are to show up in the English language for each position in the word. Humans can make guesses as they please, but WordleBot will give their best guess to help. 

## How to play
To play with an Advisor while playing the real Wordle game, `python3 AdvisorPlay.py`

To play with an Advisor with a randomized solution, `python3 RandomPlay.py`

To have the Wordle bot play by itself on all possible solutions, `python3 SelfPlay.py`
