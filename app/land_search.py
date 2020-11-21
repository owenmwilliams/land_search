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
# from docopt import docopt

# # if __name__ == '__main__':
# #     arguments = docopt(__doc__, version='land_search v0.1')
# #     print(arguments)


"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    land_search tcp <host> <port> [--timeout=<seconds>]
    land_search lucky
    land_search serial <port> [--baud=<n>] [--timeout=<seconds>]
    land_search (-i | --interactive)
    land_search (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
from docopt import docopt, DocoptExit
import main


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

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
    prompt = '(my_program) '
    file = None

    @docopt_cmd
    def do_tcp(self, arg):
        """Usage: tcp <host> <port> [--timeout=<seconds>]"""

        print(arg)

    @docopt_cmd
    def do_lucky(self, arg):
        """Usage: lucky"""
        main.lucky()

    @docopt_cmd
    def do_serial(self, arg):
        """Usage: serial <port> [--baud=<n>] [--timeout=<seconds>]
Options:
    --baud=<n>  Baudrate [default: 9600]
        """

        print(arg)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)