"""
Usage:
  toxprint_generator [--help --version --output <file> --force ]

Options:
  -h, --help                  Show this screen.
  -v, --version               Shows the program version.
  -f, --force                 Force an update to all Toxprints.
  -o <file>, --output <file>  Specify a new output path.

"""

import os, sys
newsyspath = os.path.realpath(__file__).split('\\')[:-2]
if len(newsyspath) == 0:
    newsyspath = os.path.realpath(__file__).split('/')[:-2]
    sys.path.append('/'.join(newsyspath))
else:
    sys.path.append('\\'.join(newsyspath))

from docopt import docopt
import sys
from colorama import init, Fore
# initilize colorama colored CLI text
init(autoreset=True)

from Toxprint_generator import mktoxprints
from SQL_toxprint_checker import check
from SQL_fill_txp import filldatabase
from Toxprint_force_update import update_toxprint_database

def main():
    args = docopt(__doc__)
    # print(args)

    if args['--version']:
        print('NCCT CLI: Version 0.0.0')
        sys.exit(0)

    # set input arguments and options to variables
    o = args['--output']
    f = args['--force']
    if not o:
        o = ''


    try:
        print(Fore.LIGHTGREEN_EX + '-- Checking DTXCIDs for Toxprints --')
        dtxcid2, fulldtxcid = check(f)
    except:
        print(Fore.RED + 'Error: DTXCID check failed')
        sys.exit(0)

    if dtxcid2:
        ### GENERATES TOXPRINTS FOR FINAL DTXCID LIST ###

        try:
            print(Fore.LIGHTGREEN_EX + '-- Generating Toxprints --')
            toxprintdf = mktoxprints(list(dtxcid2))
        except:
            print(Fore.RED + 'Error: Toxprint Generating Failure')
            sys.exit(1)

        ### ADDS TOXPRINT DATA TO QSAR.COMPOUND_DESCRIPTOR_SETS ###

        try:
            print(Fore.LIGHTGREEN_EX + '-- Adding Toxprints to Database --')
            filldatabase(toxprintdf)
        except:
            print(Fore.RED + 'Error: Failure Adding Toxprints to Database')
            sys.exit(1)

    # Forces an update of all Toxprints
    if f:
        # print("fulldtxcid list info")
        # print(len(fulldtxcid), fulldtxcid[0:10], fulldtxcid[-10:])
        try:
            print(Fore.LIGHTGREEN_EX + '-- Making Toxprints For Updates --')
            toxprintdf2 = mktoxprints(list(fulldtxcid))
        except:
            print(Fore.RED + '-- Error: Toxprint Generation Failure --')
            sys.exit(1)

        try:
            print(Fore.LIGHTGREEN_EX + '-- Updating All Toxprints --')
            update_toxprint_database(toxprintdf2)
        except:
            print(Fore.RED + 'Error: Failure Updating Toxprints')
            sys.exit(1)

    ### CREATES OPTIONAL OUTPUT FILE ###

    if o=='':
        pass
    else:
        try:
            print(Fore.LIGHTGREEN_EX + '-- Creating Output Table {} --'.format(o))
            toxprintdf.to_csv(o, sep='\t')
        except:
            print(Fore.RED + 'Error: Failure Exporting Toxprint File {}'.format(o))
            sys.exit(1)

    print(Fore.LIGHTGREEN_EX + '-- FINISHED --')
    sys.exit(0)

