"""
Usage:
  NCCT sid2cid (<tsv_file>|[-]) [--help --version --output <file> --noerror]
  NCCT casrn2cid (<tsv_file>|[-]) [--help --version --output <file> --noerror]
  NCCT cid2sid (<tsv_file>|[-]) [--help --version --output <file> --noerror]
  NCCT fill_fp [--help --version --output <file> --duplicate=K]
  NCCT enrich [--help --version --output <file>]
  NCCT fp_combo [--help --version --output <file>]
  NCCT gen_fp [--help --version]
  NCCT update_datasets [--help --version]
  NCCT [--help --version]

Options:
  -h, --help                  Show this screen.
  -v, --version               Shows the program version.
  -o <file>, --output <file>  Output File (instead of stdout).
  -e, --noerror               Removes error messages.
  -d=K, --duplicate=K         Handle duplicate IDs: 0=include all, 1=discard all, 2=include most frequent[default: 0].
"""

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
    print(args)
    if args['--version']:
        print('NCCT CLI: Version 0.0.0')
        sys.exit(0)
    tsv_input = args['<tsv_file>']
    o = args['--output']
    noerror = args['--noerror']


    # creates table of .tsv file
    # takes stdin if argument is not directly given
    if not tsv_input:
        tsv_input = sys.stdin.read()
        mytable = pd.read_csv(StringIO(tsv_input), sep="\t")
    elif tsv_input:
        mytable = pd.read_csv(tsv_input, sep="\t")

    # checks the index, and first two columns for DTXSIDs
    # input table should be in the correct format already
    try:
        if mytable.iloc[0,0][0:6] == 'DTXSID':
            idrow = mytable.iloc[:, 0]
            colname = mytable.columns.values[0]

    except:
        pass
    try:
        if mytable.iloc[0,1][0:6] == 'DTXSID':
            idrow = mytable.iloc[:, 1]
            colname = mytable.columns.values[0]

    except:
        pass
    try:
        if mytable.index.values[0][0:6] == 'DTXSID':
            idrow = mytable.index.values
            mytable.index.name = 'DTXSID'
            colname = mytable.index.name
    except:
        pass

    # make an SQL query table  for relevant SIDs & CIDs
    mysession = SQLSession(Schemas.dsstox_schema).get_session()

    query = mysession.query(GenericSubstances.dsstox_substance_id, Compounds.dsstox_compound_id).join(GenericSubstanceCompounds) \
        .join(Compounds).filter(GenericSubstances.dsstox_substance_id.in_(idrow))

    # checks if DTXSID didn't exist or has no associated DTXCID
    df = pd.DataFrame(list(query))

    # if no DTXCIDs returned
    if df.empty and not noerror:
        print(Fore.RED + "Error: No valid DTXSIDs or no associated DTXCIDs\n{}".format(list(idrow)))
        sys.exit(1)
    elif df.empty:
        sys.exit(1)

    noid = list(set(idrow)-set(list(df.iloc[:, 0])))

    # creates new CID table
    mytable = mytable.rename(columns={colname : "dsstox_substance_id"})
    mytable = pd.merge(df, mytable, on='dsstox_substance_id')
    mytable = mytable.drop('dsstox_substance_id', 1)
    outputtable = mytable

    # generates a string with tab seperation and line breaks for row ends
    columnnames = mytable.columns.values
    output = ''
    for i in columnnames:
        output += i + '\t'
    output += '\n'
    mytable = mytable.values.tolist()

    for i in mytable:
        a = '\t'.join(str(x) for x in i)
        output += a + '\n'

    # output options
    if not o:
        print(output)
    else:
        outputtable.to_csv(o, sep='\t', index=False)

    # ERROR message
    # not actual STDERR this is for the user
    if not noerror:
        print(Fore.RED + "Error: Invalid DTXSID or no associated DTXCID\n{}".format(noid))

if __name__ == '__main__':
    main()
