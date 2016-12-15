import os


_dir = os.path.dirname(os.path.abspath(__file__))
picks_path = os.path.join(_dir, 'powerball_picks.json')

welcome_string = 'Welcome to the Powerball CLI. Please enter a command:\n\n'
command_string = '\
    list                    list all player\'s Powerball numbers\n\
    add <full name>         add or overwrite a player\'s Powerball numbers (name optional)\n\
    delete <full name>      delete a player (name optional)\n\
    powerball               display all players\' Powerball numbers and the winning numbers\n\
    help <cmd>              show docstring of <cmd>\n\
    exit                    save the current Powerball numbers to {0} and exit\n'.format(picks_path)