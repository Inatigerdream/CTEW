import os, sys
newsyspath = os.path.realpath(__file__).split('\\')[:-2]
if len(newsyspath) == 0:
    newsyspath = os.path.realpath(__file__).split('/')[:-2]
    sys.path.append('/'.join(newsyspath))
else:
    sys.path.append('\\'.join(newsyspath))

import sys
import click
import pandas as pd
from make_special_toxprints import mk_special_fingerprints
from Special_Toxprints_checker import check
from Special_Toxprints_fill_table import filldatabase
from force_update import updatedatabase

@click.command()
@click.option('-f', is_flag=True, default=False,
    help='force an update on special toxprint fingerprints (changes to the fingerprint)')
def cli(f):
    ### HELP DOCUMENTATION ###

    """

    Checks the DATABASE for special manually created toxprints (ie combinations of toxprints). If they don't exist it generates them and adds them to the DATABASE \n
    Starts with DTXCID seperator = linebreak

    use -f force an update of full set of fingerprints. Used for changes made to fingerprints. Runs after adding new DTXCIDs.
    use -o ~/mypath/myfilename.tsv to export a toxprint .tsv file


    """

    ### CHECK IF DTXCIDS EXIST & HAVE TOXPRINTS ###
    # returns list of DTXCIDS w/o toxprints
    # if --force: return all DTXCIDs

    try:
        click.secho('-- Checking DTXCIDs for Toxprints --', bold=True)
        newdtxcid, fulldtxcid = check(f)
    except:
        click.secho('Error: DTXCID check failed', fg='red', bold=True)
        sys.exit(1)

    ### GENERATES SPECIAL TOXPRINTS FOR FINAL DTXCID LIST ###
    if newdtxcid:
        try:
            click.secho('-- Making Special Toxprints --', bold=True)
            toxprintdf = mk_special_fingerprints(newdtxcid)
        except:
            click.secho('-- Error: Special_Toxprint Generation Failure --',fg='red', bold = True)
            sys.exit(1)


    ### ADDS TOXPRINT DATA TO QSAR.COMPOUND_DESCRIPTOR_SETS ###
        try:
            click.secho('-- Adding Toxprints to Database --', bold=True)
            filldatabase(toxprintdf)
        except:
            click.secho('Error: Failure Adding Toxprints to Database', fg='red', bold=True)
            sys.exit(1)

    if f:
        try:
            click.secho('-- Making Special Toxprints --', bold=True)
            toxprintdf2 = mk_special_fingerprints(fulldtxcid)
        except:
            click.secho('-- Error: Special_Toxprint Generation Failure --',fg='red', bold = True)
            sys.exit(1)

        try:
            click.secho('-- Updating All Special Toxprints --', bold=True)
            updatedatabase(toxprintdf2)
        except:
            click.secho('Error: Failure Updating Special Toxprints', fg='red', bold=True)
            sys.exit(1)

    click.secho('-- FINISHED --', bold=True)
    sys.exit(0)