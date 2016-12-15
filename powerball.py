import cmd
import shutil
import json
import random
import config
from ordinal import ordinal

class Powerball(cmd.Cmd):
    """Command line Powerball tool"""

    prompt = 'powerball-cli: '
    doc_header = 'Commands'

    # Load existing Powerball numbers as a dict from saved json file, or empty dict if no valid json file exists
    try:
        picks_file = open(config.picks_path, 'r')
        try:
            picks = json.load(picks_file)
        except ValueError, e:
            print 'Invalid JSON data in {0}. Initializing new file.\nBad file has been copied to {0}.err'.format(
                config.picks_path)
            shutil.move(config.picks_path, config.picks_path + '.err')
            print 'Tried to load a dict but failed, making empty dict'
            picks = dict()
    except IOError, e:
        print 'Making empty dict'
        picks = dict()


    def __repr__(self):
        # Override the class instance text to something useful
        return '\n\nWelcome to the Powerball Admin Interface\n\n' + config.command_string


    def do_EOF(sel, argf):
        """Ctrl-C to break out of CLI, without saving changes"""
        return True


    def do_exit(self, arg):
        """Save the current Powerball numbers to a JSON file and exit"""
        with open(config.picks_path, 'w') as file:
            json.dump(self.picks, file)
        return True


    def do_list(self, arg):
        """Print out a list of everyone's Powerball numbers"""
        for pick in self.picks:
            print '{0}: {1}, Powerball: {2}'.format(pick.ljust(max([len(p) for p in self.picks])),
                                                    ', '.join([str(p).rjust(2) for p in self.picks[pick][:-1]]),
                                                    str(self.picks[pick][-1]).rjust(2))


    def do_delete(self, arg):
        """Delete a user, full name as optional argument"""
        if arg:
            # If an argument was provided, treat it as the full name of the user to be deleted
            full_name = arg
        else:
            # Otherwise prompt for the user to be deleted
            first_name = raw_input('First name: ')
            last_name = raw_input('Last name: ')
            full_name = ' '.join([first_name, last_name])

        # Check if the name provided has an entry (case insensitive)
        if full_name.upper() in [p.upper() for p in self.picks]:
            pick = [p for p in self.picks if p.upper() == full_name.upper()][0]
            # Make a nice readable string of their Powerball numbers
            pick_string = '{0}: {1}, Powerball: {2}'.format(pick,
                                                    ', '.join([str(p).rjust(2) for p in self.picks[pick][:-1]]),
                                                    str(self.picks[pick][-1]).rjust(2))
            prompt = 'About to delete the following user:\n{0}\nAre you sure? Y/N: '.format(pick_string)
            confirm = ''
            while confirm.upper() not in ['Y','N']:
                confirm = raw_input(prompt)
            if confirm.upper() == 'Y':
                del self.picks[pick]
                print 'Deleted ' + pick
        else:
            print '{0} not found!\nUse \'list\' to view current Powerball entries'.format(full_name)
            return

    def do_add(self, arg):
        """Add a or replace a player's Powerball numbers"""
        full_name = ''
        while len(full_name.strip()) == 0:
            first_name = raw_input('First name: ')
            last_name = raw_input('Last name: ')
            full_name = ' '.join([first_name, last_name])

        # If we have an existing dict of Powerball picks and the player is already in it (case insensitive),
        # prompt for overwrite
        if self.picks and full_name.upper() in [p.upper() for p in self.picks]:
            pick = [p for p in self.picks if p.upper() == full_name.upper()][0]
            pick_string = '{0}: {1}, Powerball: {2}'.format(pick,
                                                            ', '.join([str(p).rjust(2) for p in self.picks[pick][:-1]]),
                                                            str(self.picks[pick][-1]).rjust(2))
            overwrite = ''
            while overwrite.upper() not in ['Y', 'N']:
                overwrite = raw_input('{0} already has the following picks:\n{1}\nOverwrite? Y/N: '.format(
                    full_name, pick_string))

            # If overwrite is confirmed, delete the entry and continue. Otherwise, bail.
            if overwrite.upper() == 'Y':
                del self.picks[pick]
            else:
                return

        # Instantiate the entry as an empty list
        self.picks[full_name] = []
        # The first 5 are unique number picks between 1 and 69
        for i in range(1, 6):
            prompt = '{0} pick (1 to 69'.format(ordinal(i))
            # Include a warning about the existing selections for picks beyond the 1st
            if i > 1:
                prompt += ', excluding {0}'.format(', '.join([str(p) for p in self.picks[full_name]]))
            prompt += '): '
            new_pick = 0
            while new_pick < 1 or new_pick > 69 or new_pick in self.picks[full_name]:
                # Make sure they select an integer meeting our criteria
                try:
                    new_pick = int(raw_input(prompt))
                except:
                    print 'You must enter a number between 1 and 69, excluding {0}'.format(
                        ', '.join([str(p) for p in self.picks[full_name]]))
                    continue
            self.picks[full_name].append(new_pick)

        # The final (6th) pick is the Powerball pick between 1 and 26
        powerball_pick = 0
        while powerball_pick < 1 or powerball_pick > 26:
            # Make sure they select an integer meeting our criteria
            try:
                powerball_pick = int(raw_input('Powerball pick (1 to 26): '))
            except:
                print 'You must enter a number between 1 and 26!'
                continue
        self.picks[full_name].append(powerball_pick)


    def do_powerball(self, arg):
        """Calculate and print the winning combination, which is the most frequent number for each choice"""
        powerball_winner = []
        # Iterate through the choices in order (1st picks for all users, 2nd, 3rd, 4th, 5th, and the Powerball)
        for i in range(6):
            # Make a list of all choices made for this index
            # This isn't part of the written requirements, but I'm excluding numbers that have already been chosen
            # Otherwise, the same choice could be most frequent in two positions and result in an impossible combination
            if i < 5:
                all_picks = [p[i] for p in [self.picks[u] for u in self.picks] if p[i] not in powerball_winner]
            # For the Powerball (6th choice), don't exclude numbers already chosen for the winning combination
            else:
                all_picks = [p[i] for p in [self.picks[u] for u in self.picks]]

            # Make a list of unique numbers for this index
            unique_picks = [up for up in set(all_picks)]

            # Get the maximum count of the most frequent choices, in case there are ties
            max_count = all_picks.count(max(all_picks, key=all_picks.count))

            # Get the unique numbers chosen the max number of times and pick a random one
            pick = random.choice([n for n in unique_picks if all_picks.count(n)==max_count])
            powerball_winner.append(pick)

        # Print the list of entries
        for pick in self.picks:
            print '{0}: {1}, Powerball: {2}'.format(pick.ljust(max([len(p) for p in self.picks])),
                                                    ', '.join([str(p).rjust(2) for p in self.picks[pick][:-1]]),
                                                    str(self.picks[pick][-1]).rjust(2))

        # Print the winning combo
        print '\nPowerball Winner: {0}, Powerball: {1}'.format(', '.join([str(p).rjust(2) for p in powerball_winner[:-1]]),
                                                               str(powerball_winner[-1]).rjust(2))
        winners = [p for p in self.picks if self.picks[p] == powerball_winner]
        if winners:
            print 'Winners! {0}'.format(', '.join(winners))
        else:
            print 'Nobody won! :-('