import os, sys
newsyspath = os.path.realpath(__file__).split('\\')[:-2]
if len(newsyspath) == 0:
    newsyspath = os.path.realpath(__file__).split('/')[:-2]
    sys.path.append('/'.join(newsyspath))
else:
    sys.path.append('\\'.join(newsyspath))

import math
from database.dsstox.compounds import Compounds
from database.database_schemas import Schemas
from database.session import SQLSession
from database.qsar.descriptors import Descriptors
from database.qsar.datapoints import Datapoints
from database.qsar.datasets import Datasets
from database.qsar.dataset_datapoints import DatasetDatapoints
from database.qsar.statistics import Statistics
from database.qsar.uc_statistics import UcStatistics
from database.qsar.univariate_calculations import UnivariateCalculations
from sqlalchemy import or_, and_, any_
import sys
import pandas as pd
from Enrichment_to_MySQL.duplicatehandler import handle_duplicates
from Enrichment_to_MySQL.enrichment import enrich
from Enrichment_to_MySQL.fillfp1 import fillfp
import time
from multiprocessing import Pool

### HELP DOCUMENTATION ###

"""
checks for updates for Datasets.id (new compounds / new endpoints / new AEIDS)

if there are any updates this script will generate new enrichment tables for that Dataset.id

the DATABASE is then updated to include the new enrichment tables

"""

########################################################################################################################

### ADD ENRICHMENTTABLE & DATATABLE TO MYSQL DATABASE
# Takes a table & a single AEID
# fills mysql uc_statistics & univariate_calculations w/ aeid, hitc, and DTXCID info

def filluc(invitrodbdf, mydatasetid):
    #set starttime
    starttime = time.time()

    username = 'rlougee'
    descriptor_set_id = [1445, 1447, 1446, 1448]
    # descriptor_set_id = [1448] # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 1445 = toxprints
    # 1446 = MACCS
    # 1447 = pubchem
    # 1448 = Special Toxprints

    for id in descriptor_set_id:
        # add enrichment table to the mysql database
        try:
            filled_table = handle_duplicates(invitrodbdf.loc[:, ['dsstox_compound_id', 'hitc']])

        except:
            print("DUPLICATE HANDLER FAILED: {}".format(mydatasetid))
            sys.exit(1)

        try:
            filled_table = fillfp(filled_table, id)
        except:
            print("FILLFP FAILED: {}".format(mydatasetid))
            sys.exit(1)

        # filled_table = pd.DataFrame(filled_table)

        try:
            my_enrichment_table = enrich(filled_table)

        except:
            print("ENRICH FAILED: {}".format(mydatasetid))
            print(filled_table.head())
            sys.exit(1)


        # add fk_descriptor_id
        ### CHECK THAT THESE ARE MATCHING! ###
        mysession2 = SQLSession(Schemas.qsar_schema).get_session()
        query3 = mysession2.query(Descriptors.id).filter(Descriptors.fk_descriptor_set_id == id)
        query3 = list(query3)
        query3 = [int(i[0]) for i in query3]
        my_enrichment_table.insert(0, 'fk_descriptor_id', query3)

        for index, row in my_enrichment_table.iterrows():
            fk_dataset_id = int(mydatasetid)
            fk_descriptor_id = int(row['fk_descriptor_id'])

            univariate_calc = UnivariateCalculations(fk_dataset_id=fk_dataset_id,
                                                     fk_descriptor_id=fk_descriptor_id,
                                                     updated_by=username,
                                                     created_by=username)
            mysession2.add(univariate_calc)
            mysession2.flush()

            fk_univ_calc_id = int(univariate_calc.id)

            ### NEED TO CHANGE for loop & stat_list IF THE STATISTICS ARE CHANGED IN Enrichment_Table_Generator ###
            count = 0
            for i in row[1:]:

                if math.isnan(i):
                    value = None
                elif math.isinf(i):
                    value = 99999999.9
                else:
                    value = float(i)

                stat_list = [9, 10, 11, 12, 13, 4, 8, 7, 14, 15]
                fk_statistic_id = int(stat_list[count])

                uc_statistics = UcStatistics(value=value,
                                             fk_univ_calc_id=int(fk_univ_calc_id),
                                             fk_statistic_id=int(fk_statistic_id),
                                             created_by=username,
                                             updated_by=username)

                mysession2.add(uc_statistics)
                count += 1
        mysession2.commit()
        # mysession2.close()
    endtime = time.time()
    print('run time:{}'.format(endtime-starttime))

########################################################################################################################

# begin a for loop for each unique aeid
def fillnewenrich(x_aeid):
    # retrive the latest dataset for the aeid
    new_df = query1[query1['name'].isin([x_aeid])]
    # rename columns
    new_df.columns = ['dsstox_compound_id', 'hitc', 'name', 'dataset_id']
    my_dataset_id = new_df['dataset_id'].iloc[0]
    # make the enrichment table
    filluc(new_df, my_dataset_id)


########################################################################################################################

### QUERY DATE WHEN THE TABLE WAS LAST UPDATED ###
# Not very useful as datasets.name date will always be different/ not worth querying all of the dates

# query1 = mysession.query(Tables.UPDATE_TIME)\
#     .filter(or_(Tables.TABLE_SCHEMA == 'invitrodb'), (Tables.TABLE_NAME == 'mc5'))
#
# #format last_update query
# last_update = str(list(query1)[0][0])[:10].replace('-','')

########################################################################################################################

#begin a for loop for each unique aeid
# for x_aeid in query1.name.unique():
#     #check speed of program
#     starttime = time.time()
#     # retrive the latest dataset for the aeid
#     new_df = query1[query1['name'].isin([x_aeid])]
#     # rename columns
#     new_df.columns = ['dsstox_compound_id', 'hitc', 'name', 'dataset_id']
#     my_dataset_id = new_df['dataset_id'].iloc[0]
#     # make the enrichment table
#     filluc(new_df, my_dataset_id)

####################################################################################################################

# create a connection pool for multiprocessing with mysqlalchemy
if __name__ == '__main__':

    ### QUERY THE MYSQL DB 4 A COMPLETE LIST OF AEIDS, ENDPOINTS & DTXCIDS ###

    mysession = SQLSession(Schemas.qsar_schema).get_session()

    # query the Unique Enrichment Table IDs
    query0 = mysession.query(UnivariateCalculations.fk_dataset_id)
    query0 = pd.DataFrame(list(query0))

    if query0.empty:
        pass
    else:
        query0 = query0.fk_dataset_id.unique()

    # query the full set of data
    # slow ~3.5 minutes already
    query1 = mysession.query(Compounds.dsstox_compound_id, Datapoints.measured_value_dn, Datasets.name, Datasets.id) \
        .join(Datapoints, Datapoints.efk_dsstox_compound_id == Compounds.id) \
        .join(DatasetDatapoints, Datapoints.id == DatasetDatapoints.fk_datapoint_id) \
        .join(Datasets, DatasetDatapoints.fk_dataset_id == Datasets.id)

    query1 = pd.DataFrame(list(query1))

    # remove tables with Enrichments already made
    query1 = query1[~query1['id'].isin(query0)] #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # if query1 is empty exit
    if query1.empty:
        print('Enrichments are up to date')
        sys.exit(0)

    starttime = 0

    p = Pool(20)
    p.map(fillnewenrich, query1.name.unique())

    # sys.exit(0)
    # for i in query1.name.unique():
    #     starttime = time.time()
    #     fillnewenrich(i)