"""
Usage:
  removeduplicates (<tsv_file>|[-]) (--anyhit | --mostfrequent | --fullremove) [--help --version --output <file> --error ]

Options:
  -h, --help                  Show this screen.
  -v, --version               Shows the program version.
  -o <file>, --output <file>  Specify a new output path.
  --anyhit                    If id has any hits id is considered positive.
  --mostfrequent              Uses most frequent hitcall for id.
  --fullremove                Removes any duplicate ids.
  -e, --error                 Adds error message for duplicate IDs.
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
from database.session import SQLSession
import sys
from io import StringIO
import os
import pandas as pd
from colorama import init, Fore
# initilize colorama colored CLI text
init(autoreset=True)

### Function which ignores, deletes, or selects most frequent ID endpoints with duplicates ###

def main():
    args = docopt(__doc__)
    # print(args)

    if args['--version']:
        print('NCCT CLI: Version 0.0.0')
        sys.exit(0)

    # set input arguments and options to variables
    tsv_input = args['<tsv_file>']
    o = args['--output']
    error = args['--error']
    anyhit = args['--anyhit']
    mostfrequent = args['--mostfrequent']
    fullremove = args['--fullremove']

    # creates table of .tsv file
    # takes stdin if argument is not directly given
    if not tsv_input:
        tsv_input = sys.stdin.read()
        table = pd.read_csv(StringIO(tsv_input), sep="\t")
    elif tsv_input:
        table = pd.read_csv(tsv_input, sep="\t")

    # set mypass
    if anyhit:
        mypass = 3
    elif mostfrequent:
        mypass = 2
    elif fullremove:
        mypass = 1

    myid = table.columns[0]

    if mypass > 3 or mypass < 0:
        print('invalid duplicate id')
        sys.exit(0)
    else:
        pass

    # need to sort table
    table = table.sort_values([table.columns.values[0],table.columns.values[1]])
    table = table.reset_index(drop=True)

    # create an empty list for that will contain rows to drop
    droplist = []
    lastid = 0
    count = 0

    # if any duplicate id has a hit row is considered a positive hit
    if mypass == 3:
        for i, row in zip(table.duplicated(subset=myid, keep='last'), table.iterrows()):
            if i == True:
                droplist.append(row[0])
    elif mypass == 2:
        table = table.groupby(myid, as_index=False).mean()
        table = table.dropna(axis=1)
    elif mypass == 1:
        table = table.drop_duplicates(subset=myid, keep=False)

    # drop the extra rows
    table = table.drop(droplist)

    # make sure column is int
    table.iloc[:,1:] = table.iloc[:,1:].astype(int)

    # reset index
    table = table.reset_index(drop=True)
    table = table.dropna(axis='columns')

    # setup string for std out
    mytable = table.iloc[:, :]
    columnnames = table.columns.values
    output = ''
    for i in columnnames:
        output += i + '\t'
    output += '\n'
    mytable = mytable.values.tolist()

    for i in mytable:
        a = '\t'.join(str(x) for x in i)
        output += a + '\n'

    # output
    if o:
        table.to_csv(o, sep='\t', index=False)
    else:
        print(output)

# # TEST # # #
if __name__=='__main__':
    import pandas as pd
    a = [['DTXCID101', 0], ['DTXCID101', 0], ['DTXCID101', 1], ['DTXCID202', 1], ['DTXCID202', 1], ['DTXCID303', 0], ['DTXCID303', 0], ['DTXCID404', 0], ['DTXCID101', 0]]
    a = pd.DataFrame(a)
    print('any hit', main())
    print('most_frequent', main())
    print('remove', main())
    print('leave', main())