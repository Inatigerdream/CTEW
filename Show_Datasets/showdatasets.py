"""ShowDatasets will show all the datasets containing a given string.
wild cards: _ = any one character; % = any length of any characters

Usage:
  showdatasets (<InputString>|[-]) [--help --version]

Options:
  -h, --help                  Show this screen.
  -v, --version               Shows the program version.
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
import sys
import pandas as pd
from io import StringIO
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
    InputString = args['<InputString>']
    if not InputString:
        InputString = sys.stdin.read()

    mysession = SQLSession(Schemas.dsstox_schema).get_session()
    query = mysession.execute('SELECT datasets.name FROM sbox_rlougee_qsar.datasets WHERE datasets.name LIKE "%{}%"'.format(InputString))
    for i in pd.DataFrame(list(query))[0]:
        print(i)

if __name__ == '__main__':
    main()
