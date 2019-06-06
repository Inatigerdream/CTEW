from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.session import SQLSession
import sys
import pandas as pd
import subprocess as subp
import glob

# create a tsv with dataset name x TP/TOTAL_CHEM so that we can see the coverage of our Toxprint Models

# get all relevant datasets
mysesson = mysession = SQLSession(Schemas.qsar_schema).get_session()

datasets = [x[0] for x in mysession.execute('SELECT datasets.name FROM sbox_rlougee_qsar.datasets'
                                 ' WHERE sbox_rlougee_qsar.datasets.name LIKE "%Ori\_MC%"')]

print(len(datasets))

# get TP stats file for each dataset
# for i in datasets[1053:]:
#     print(i)
#     command = subp.Popen('pullenrichment {} --fpenrich -o "/share/home/rlougee/Desktop/ori_mc_percent_coverage/"'.format(i), shell=True)
#     command.communicate()

