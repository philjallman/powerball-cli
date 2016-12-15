# powerball-cli
Interactive CLI to manage a Powerball game

Run `python main.py` to launch the interface, which will accept the following commands:
```
    list                    list all player's Powerball numbers
    add <full name>         add or overwrite a player's Powerball numbers (name optional)
    delete <full name>      delete a player (name optional)
    powerball               display all players' Powerball numbers and the winning numbers
    help <cmd>              show docstring of <cmd>
    exit                    save the current Powerball numbers to {0} and exit
```

The winning Powerball combination is calculated as follows:

From the list of entries (sample file `powerball_picks.json`), the most frequent choice in each of slots 1 through 5 is
selected as the winner, provided that number hasn't been chosen in a prior slot. The most frequent choice in the 6th and
final slot is selected regardless of whether it has appeared in the winning numbers already. In all cases of a tie in
frequency, a random selection is made from the most frequent choices.
