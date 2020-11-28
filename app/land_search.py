# """land_search
# Usage:
#   land_search.py estimate_cty [--radius=<deg> --pop=<perc> | --comp_num=<num>] (<cty_fips>...)
#   land_search.py refresh_data [<table_name>] (-spot | -full)
#   land_search.py refresh_estimate (-spot | -full)
#   land_search.py rank_cty <model_params> <cty_fips>...
#   land_search.py fltr_cty <model_params>
#   land_search.py cty_data <cty_fips>...
# Options:
#   -help           Show this screen.
#   -version        Show version.
#   --radius=<deg>  Radius to find comparable counties in deg lat / long. [default: 2].
#   --pop=<perc>    Population percent +/- on county being estimated. [default: 1].
# """

"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    land_search find_lucky
    land_search find_state <state>...
    land_search estimate (params [--radius=<deg> --pop=<percent>] | comps [--comps=<number>]) (<cty_fips>...)
    land_search test <arguments>...
    land_search (-i | --interactive)
    land_search (-h | --help)
    land_search (-v | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help         Show this screen and exit
    -v, --version      Show version
    --radius=<deg>     Radius to search within for comparable counties in deg lat / long [default: 2]
    --pop=<percent>    Population percent +/- on county being estimated [default: 1]
    --comps=<number>   Number of comps requested for a given county estimation [default: 5]
"""

import sys
import cmd
from docopt import docopt, DocoptExit
import main
import pandas as pd

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg, version='v0.1')

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = '(land_search) '
    file = None

    pd.set_option('display.max_rows', None)

    @docopt_cmd
    def do_find_lucky(self, arg):
        """Usage: find_lucky"""
        county = main.find_lucky()
        print('*********************************************************')
        print(county)

    @docopt_cmd
    def do_find_state(self, arg):
        """Usage: find_state <state>..."""      
        for _ in range(len(arg['<state>'])):
            state = arg['<state>'][_]
            array = main.find_state(state)
            if len(array) > 0:
                print('*********************************************************')
                print(array)
            else:
                try:
                    state = arg['<state>'][_] + ' ' + arg['<state>'][_+1]
                    array = main.find_state(state)
                    if len(array) > 0:
                        print('*********************************************************')
                        print(array)
                except:
                    break

    @docopt_cmd
    def do_estimate(self, arg):
        """Usage: estimate (params [--radius=<deg> --pop=<percent>] | comps [--comps=<number>]) (<cty_fips>)...

            Options:
            --radius=<deg>     Radius to search within for comparable counties in deg lat / long. [default: 2]
            --pop=<percent>    Population percent +/- on county being estimated. [default: 1]
            --comps=<number>   Number of comps requested for a given county estimation. [default: 5]
        """
        if arg['params'] is True:
            for _ in range(len(arg['<cty_fips>'])):
                main.params_estimate(arg['--pop'], arg['--radius'], arg['<cty_fips>'][_])
        elif arg['comps'] is True:
            for _ in range(len(arg['<cty_fips>'])):
                main.comps_estimate(arg['--comps'], arg['<cty_fips>'][_])

    @docopt_cmd
    def do_test(self, arg):
        """Usage: test <arguments>..."""
        for _ in range(len(arg['<arguments>'])):
            print(arg['<arguments>'][_])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:], version='v0.1')

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)