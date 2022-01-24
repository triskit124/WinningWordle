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
If you are a human wishing to have a robotic Wordle advisor, `python3 UserPlay.py`

If you are a robot wishing to play Wordle at lighting speed, `python3 SelfPlay.py`
