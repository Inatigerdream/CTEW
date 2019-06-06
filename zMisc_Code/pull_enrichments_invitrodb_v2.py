from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import sys
import pandas as pd
import subprocess as subp
import glob
from multiprocessing import Pool

def com(i):
    print(i)
    command = subp.Popen(
        'pullenrichment "{}%" --fpenrich -o "/share/home/rlougee/Desktop/invitrodb_v2_enrichments/"'.format(i),
        shell=True)
    command.communicate()

# create a tsv with dataset name x TP/TOTAL_CHEM so that we can see the coverage of our Toxprint Models

# get all relevant datasets
mysession = SQLSession(Schemas.qsar_schema).get_session()

datasets = [x[0] for x in mysession.execute('SELECT datasets.name FROM sbox_rlougee_qsar.datasets'
                                 ' WHERE sbox_rlougee_qsar.datasets.name LIKE "Imported_DataTable:aeid\_%\_invitrodbv2\_20180918"')]

# print(len(datasets))
# print(datasets[180:])
# sys.exit(1)
# # get TP stats file for each dataset
# for i in datasets[38:]:
#     print(i)
#     sys.exit(0)
#     command = subp.Popen('pullenrichment "{}%" --fpenrich -o "/share/home/rlougee/Desktop/invitrodb_v2_enrichments/"'.format(i), shell=True)
#     command.communicate()


# add multiprocessing for script
p = Pool(15)
p.map(com, datasets)