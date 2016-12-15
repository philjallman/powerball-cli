# Runs an interactive CLI to manage Powerball picks for any number of users, saved in a JSON file
from powerball import Powerball

if __name__ == '__main__':
    pb = Powerball()
    pb.cmdloop(pb)