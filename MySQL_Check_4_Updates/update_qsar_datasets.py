import os, sys
newsyspath = os.path.realpath(__file__).split('\\')[:-2]
if len(newsyspath) == 0:
    newsyspath = os.path.realpath(__file__).split('/')[:-2]
    sys.path.append('/'.join(newsyspath))
else:
    sys.path.append('\\'.join(newsyspath))

import datetime
from database.database_schemas import Schemas
from database.invitrodb.mc5 import Mc5
from database.invitrodb.mc4 import Mc4
from database.invitrodb.sample import Sample
from database.dsstox.compounds import Compounds
from database.dsstox.generic_substances import GenericSubstances
from database.dsstox.generic_substance_compounds import GenericSubstanceCompounds
from database.session import SQLSession
from database.qsar.datapoints import Datapoints
from database.qsar.datasets import Datasets
from database.qsar.dataset_datapoints import DatasetDatapoints
import sys
import click
import pandas as pd

@click.command()
def cli():
    ### HELP DOCUMENTATION ###

    """
    checks for updates for AEIDS (new compounds / new endpoints / new AEIDS)

    if there are any updates qsar.datapoints, qsar.datasets, and qsar.datasetdatapoints are updated to include this information

    """

    ####################################################################################################################

    #QUERY MC5 data for hitcalls and chemical IDs

    mysession = SQLSession(Schemas.information_schema).get_session()

    query0 = mysession.query(Compounds.id, Compounds.dsstox_compound_id, Mc5.hitc, Mc5.aeid) \
        .join(GenericSubstanceCompounds, Compounds.id == GenericSubstanceCompounds.fk_compound_id) \
        .join(GenericSubstances, GenericSubstances.id == GenericSubstanceCompounds.fk_generic_substance_id) \
        .join(Sample, Sample.chid == GenericSubstances.id) \
        .join(Mc4, Mc4.spid == Sample.spid) \
        .join(Mc5, Mc5.m4id == Mc4.m4id)

    mc5_table = pd.DataFrame(list(query0))

    ####################################################################################################################

    ### QUERY DATE WHEN THE TABLE WAS LAST UPDATED ###
    # Not very useful as datasets.name date will always be different/ not worth querying all of the dates

    # query1 = mysession.query(Tables.UPDATE_TIME)\
    #     .filter(or_(Tables.TABLE_SCHEMA == 'invitrodb'), (Tables.TABLE_NAME == 'mc5'))
    #
    # #format last_update query
    # last_update = str(list(query1)[0][0])[:10].replace('-','')
    ####################################################################################################################

    def filldatasets(invitrodbdf, fd_aeid):
        username = 'rlougee'
        # create a new datasets name entry
        datasets_name = str('aeid:{}_{}'.format(fd_aeid, datetime.datetime.today().strftime("%Y%m%d")))
        description = "The set of hit calls from the toxcast AEID: {} taken on the date:{}"\
            .format(fd_aeid, datetime.datetime.today().strftime("%Y%m%d"))
        datasets = Datasets(name=datasets_name, label=datasets_name,
                            updated_by=username, created_by=username,
                            long_description=description, short_description=description)
        mysession.add(datasets)
        mysession.flush()
        fk_dataset_id = int(datasets.id)

        # add datatable to the mysql database
        for index, row in invitrodbdf.iterrows():
            efk_dsstox_compound_id = row.loc['id']
            efk_chemprop_measured_property_id = None  #leave null -CG #not nullable
            measured_value_dn = row.loc['hitc']
            created_by = username
            updated_by = username

            datapoints = Datapoints(efk_dsstox_compound_id=efk_dsstox_compound_id,
                                    efk_chemprop_measured_property_id=efk_chemprop_measured_property_id,
                                    measured_value_dn=measured_value_dn,
                                    created_by=created_by,
                                    updated_by=updated_by)

            mysession.add(datapoints)
            mysession.flush()

            fk_datapoint_id = int(datapoints.id)

            dataset_datapoints = DatasetDatapoints(fk_dataset_id=fk_dataset_id,
                                                   fk_datapoint_id=fk_datapoint_id,
                                                   updated_by=username,
                                                   created_by=username)
            mysession.add(dataset_datapoints)
        mysession.commit()

    ####################################################################################################################

    ### CHECK 1) IF TABLE EXISTS FOR AEID 2) IF THE TABLE HAS CHANGED

    # begin a for loop for each unique aeid
    for x_aeid in mc5_table.aeid.unique():
        #query latest dataset for this aeid
        aeid_query = mysession.query(Datasets.name) \
            .filter(Datasets.name.like("aeid:{}/_%".format(str(x_aeid)), escape='/'))

        aeid_query = list(aeid_query)
        aeid_query = [x[0] for x in aeid_query]

        #get the latest values for aeid
        new_df = mc5_table[mc5_table['aeid'].isin([x_aeid])]

        if aeid_query == [] or aeid_query==[''] or aeid_query==None:

            print("New AEID, filling mysql database for aeid: {}".format(x_aeid))

            filldatasets(new_df, x_aeid)

        else:
            # find and retrieve the newest dataset name
            aeid_query_dates = [x.split('_')[1] for x in aeid_query]
            newest_aeid_date = sorted(aeid_query_dates)[0]
            newest_aeid = [x for x in aeid_query if str(newest_aeid_date) in x]

            #pull table and compare
            old_df = mysession.query(Datapoints.efk_dsstox_compound_id, Datapoints.measured_value_dn)\
                .join(DatasetDatapoints, Datapoints.id==DatasetDatapoints.fk_datapoint_id)\
                .join(Datasets, DatasetDatapoints.fk_dataset_id==Datasets.id)\
                .filter(Datasets.name==newest_aeid[0])

            old_df = pd.DataFrame(list(old_df))


            ##FORMAT DFs FOR COMPARING
            #rename columns
            old_df.columns = ['id', 'hitc']
            my_new_df = new_df.loc[:,['id', 'hitc']]
            old_df['hitc'] = old_df['hitc'].astype(int)

            #sort dataframes
            my_new_df = my_new_df.sort_values(['id', 'hitc'])
            old_df = old_df.sort_values(['id', 'hitc'])

            #reset index
            my_new_df = my_new_df.reset_index(drop=True)
            old_df = old_df.reset_index(drop=True)

            if my_new_df.equals(old_df)==True:

                print("no change for aeid: {}".format(x_aeid))

                pass

            else:

                print("Update, filling mysql database for aeid: {}".format(x_aeid))

                filldatasets(new_df, x_aeid)


    ####################################################################################################################