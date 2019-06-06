""" Cheack for any new compounds and adds Toxprint fingerprints for them.

Usage:
  ToxcastFP_generator [--help --version --force]

Options:
  -h, --help       Show this screen.
  -v, --version    Shows the program version.
  -f, --force      Forces an update of all ToxcastFP.
"""

import os, sys
newsyspath = os.path.realpath(__file__).split('\\')[:-2]
if len(newsyspath) == 0:
    newsyspath = os.path.realpath(__file__).split('/')[:-2]
    sys.path.append('/'.join(newsyspath))
else:
    sys.path.append('\\'.join(newsyspath))
from docopt import docopt
from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.dsstox.generic_substances import GenericSubstances
from database.session import SQLSession
from database.dsstox.generic_substance_compounds import GenericSubstanceCompounds
import pandas as pd
from io import StringIO
import sys
from make_toxcastfp import mk_toxcastfp
from ToxcastFP_checker import check
from ToxcastFP_fill_table import filldatabase
from ToxcastFP_force_update import updatedatabase

from colorama import init, Fore
# initilize colorama colored CLI text
init(autoreset=True)

def main():
    args = docopt(__doc__)
    # print(args)

    if args['--version']:
        print('NCCT CLI: Version 0.0.0')
        sys.exit(0)

    # set input arguments and options to variables
    f = args['--force']

    ### CHECK IF DTXCIDS EXIST & HAVE ToxcastFPs ###
    # returns list of DTXCIDS w/o toxprints
    # if --force: return all DTXCIDs

    try:
        print(Fore.LIGHTGREEN_EX + '-- Checking DTXCIDs for ToxcastFPs --',)
        newdtxcid, fulldtxcid = check(f)
    except:
        print(Fore.RED + 'Error: DTXCID check failed')
        sys.exit(1)

    ### GENERATES ToxcastFPs ###
    if not newdtxcid.empty:
        try:
            print(Fore.LIGHTGREEN_EX + '-- Making Special Toxprints --')
            toxcastfp_df = mk_toxcastfp(newdtxcid)
        except:
            print(Fore.RED + '-- Error: Special_Toxprint Generation Failure --')
            sys.exit(1)


    ### ADDS TOXPRINT DATA TO QSAR.COMPOUND_DESCRIPTOR_SETS ###
        try:
            print(Fore.LIGHTGREEN_EX + '-- Adding Toxprints to Database --')
            filldatabase(toxcastfp_df)
        except:
            print(Fore.RED + 'Error: Failure Adding Toxprints to Database')
            sys.exit(1)

    if f:
        try:
            print(Fore.LIGHTGREEN_EX + '-- Making Special Toxprints --')
            toxcastfp_df2 = mk_toxcastfp(fulldtxcid)
        except:
            print(Fore.RED + '-- Error: Special_Toxprint Generation Failure --')
            sys.exit(1)

        try:
            print(Fore.LIGHTGREEN_EX + '-- Updating All Special Toxprints --')
            updatedatabase(toxcastfp_df2)
        except:
            print(Fore.RED + 'Error: Failure Updating Special Toxprints')
            sys.exit(1)

    print(Fore.LIGHTGREEN_EX, '-- FINISHED --')
    sys.exit(0)