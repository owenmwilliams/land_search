"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    land_search find_lucky [-l]
    land_search find_state [-l] <state>...
    land_search estimate [-l] (params [--radius=<deg> --pop=<percent>] | comps [--comps=<number>]) [-l] (<cty_fips>...)
    land_search search [-l] (simple [--value=<value> --share=<percent> --population=<pop>] | complex [--value=<value> --share=<percent> --population=<pop> --air_prox=<air> --parks_prox=<parks> --parks_num=<nparks>])
    land_search test <arguments>...
    land_search (-i | --interactive)
    land_search (-h | --help)
    land_search (-v | --version)
Options:
    -i, --interactive     Interactive Mode
    -h, --help            Show this screen and exit
    -v, --version         Show version
    -l                    Run local
    --radius=<deg>        Radius to search within for comparable counties in deg lat / long [default: 2]
    --pop=<percent>       Population percent +/- on county being estimated [default: 1]
    --comps=<number>      Number of comps requested for a given county estimation [default: 5]
    --value=<value>       Maximum value to search on in $/square acre. [default: 50000]
    --share=<percent>     Maximum share of value that is attributable to land. [default: 0.25]
    --population=<pop>    Maximum population of a counties to search on. [default: 100000]
    --air_prox=<air>      Proximity of a major airport. [default: 3]
    --parks_prox=<parks>  Proximity within which to search for nearby parks. [default: 5]
    --parks_num=<nparks>  Number of parks needed within parks proximity. [default: 3]
"""

import sys
import cmd
from docopt import docopt, DocoptExit
import ssh.ssh_find as sf
import ssh.ssh_estimate as se
import ssh.ssh_search as ss
import ssh.ssh_assess as sa
import main
import pandas as pd

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg, version='v0.0.2')

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
        """Usage: find_lucky [-l]

            Options: 
            -l                 Runs local        
        """
        if arg['-l'] is False:
            sf.sf_lucky('cluster')
        else:
            main.find_lucky()

    @docopt_cmd
    def do_find_state(self, arg):
        """Usage: find_state [-l] <state>...
        
            Options: 
            -l                 Runs local
        """      
        if arg['-l'] is False:
            for _ in range(len(arg['<state>'])):
                try:
                    state = arg['<state>'][_]
                    sf.sf_state('cluster', state)
                except:
                    pass
                else:
                    try:
                        state = arg['<state>'][_] + ' ' + arg['<state>'][_+1]
                        sf.sf_state('cluster', state)
                    except:
                        pass
        else:
            for _ in range(len(arg['<state>'])):
                try:
                    state = arg['<state>'][_]
                    main.find_state(state)
                except:
                    pass
                else:
                    try:
                        state = arg['<state>'][_] + ' ' + arg['<state>'][_+1]
                        main.find_state(state)
                    except:
                        pass         

    @docopt_cmd
    def do_estimate(self, arg):
        """Usage: estimate [-l] (params [--radius=<deg> --pop=<percent>] | comps [--comps=<number>]) (<cty_fips>)...

            Options:
            --radius=<deg>     Radius to search within for comparable counties in deg lat / long. [default: 2]
            --pop=<percent>    Population percent +/- on county being estimated. [default: 1]
            --comps=<number>   Number of comps requested for a given county estimation. [default: 5]
            -l                 Runs local
        """
        if arg['params'] is True:
            if arg['-l'] is False:
                for _ in range(len(arg['<cty_fips>'])):
                    se.se_est_params('cluster', arg['--pop'], arg['--radius'], arg['<cty_fips>'][_])
            else:
                for _ in range(len(arg['<cty_fips>'])):    
                    main.params_estimate(arg['--pop'], arg['--radius'], arg['<cty_fips>'][_])
        elif arg['comps'] is True:
            if arg['-l'] is False:
                for _ in range(len(arg['<cty_fips>'])):
                    se.se_est_comps('cluster', arg['--comps'], arg['<cty_fips>'][_])
            elif arg['-l'] is True:
                for _ in range(len(arg['<cty_fips>'])):    
                    main.comps_estimate(arg['--comps'], arg['<cty_fips>'][_])

    @docopt_cmd
    def do_search(self, arg):
        """Usage: search [-l] (simple [--value=<value> --share=<percent> --population=<pop>] | complex [--value=<value> --share=<percent> --population=<pop> --air_prox=<air> --parks_prox=<parks> --parks_num=<nparks>])

            Options:
            --value=<value>       Maximum value to search on in $/square acre. [default: 50000]
            --share=<percent>     Maximum share of value that is attributable to land. [default: 0.25]
            --population=<pop>    Maximum population of a counties to search on. [default: 100000]
            --air_prox=<air>      Proximity of a major airport. [default: 3]
            --parks_prox=<parks>  Proximity within which to search for nearby parks. [default: 5]
            --parks_num=<nparks>  Number of parks needed within parks proximity. [default: 3]
            -l                    Runs local
        """
        if arg['simple'] is True:
            if arg['-l'] is False:
                ss.ss_search_simple('cluster', arg['--value'], arg['--share'], arg['--population'])
            else:
                main.search_all(arg['--value'], arg['--share'], arg['--population'])
        elif arg['complex'] is True:
            if arg['-l'] is False:
                ss.ss_search_complex('cluster', arg['--value'], arg['--share'], arg['--population'], arg['--air_prox'], arg['--parks_prox'], arg['--parks_num'])
            else:
                main.search_complex(arg['--value'], arg['--share'], arg['--population'], arg['--air_prox'], arg['--parks_prox'], arg['--parks_num'])
                
    @docopt_cmd
    def do_assess(self, arg):
        """Usage: assess [-l] [--file=<doc_path>]

            Options:
            -l                    Runs local
            --file=<doc_path>        Defines an input YAML file for variables. [default: '~/Projects/land_search/models/est/calc/defaults.yaml']
        """
        # if arg['--file'] == './est/calc/defaults.yaml':
        if arg['-l'] is False:
            sa.sa_assess('cluster', arg['--file'])
        else:
            main.assess(arg['--file'])
        # else:
            # TODO: fill out non-default path approach...

    @docopt_cmd
    def do_test(self, arg):
        """Usage: test <arguments>..."""
        for _ in range(len(arg['<arguments>'])):
            print(arg['<arguments>'][_])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
