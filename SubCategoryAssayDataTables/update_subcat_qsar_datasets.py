import os, sys
newsyspath = os.path.realpath(__file__).split('\\')[:-2]
if len(newsyspath) == 0:
    newsyspath = os.path.realpath(__file__).split('/')[:-2]
    sys.path.append('/'.join(newsyspath))
else:
    sys.path.append('\\'.join(newsyspath))
import datetime
import math
from database.session import SQLSession
from database.database_schemas import Schemas
from database.information.TABLES import Tables
from database.invitrodb.mc5 import Mc5
from database.invitrodb.mc4 import Mc4
from database.invitrodb.sample import Sample
from database.dsstox.compounds import Compounds
from database.dsstox.generic_substances import GenericSubstances
from database.dsstox.generic_substance_compounds import GenericSubstanceCompounds
from database.session import SQLSession
from database.qsar.compound_descriptor_sets import CompoundDescriptorSets
from database.qsar.descriptors import Descriptors
from database.qsar.datapoints import Datapoints
from database.qsar.datasets import Datasets
from database.qsar.dataset_datapoints import DatasetDatapoints
from database.qsar.statistics import Statistics
from database.qsar.uc_statistics import UcStatistics
from database.qsar.univariate_calculations import UnivariateCalculations
from database.invitrodb.assay_component import AssayComponent
from database.invitrodb.assay_component_endpoint import AssayComponentEndpoint
from sqlalchemy import or_, and_
import sys
import click
import pandas as pd
from io import StringIO




### HELP DOCUMENTATION ###

"""
creates datatables for assay categories

first verifies that changes have been made, then creates a new datable

"""

####################################################################################################################

#shouldn't need to change this too much

def filldatasets(invitrodbdf, fd_aeid):
    username = 'rlougee'
    # create a new datasets name entry

    datasets_name = str('assay_cat:{}_{}'.format(fd_aeid, datetime.datetime.today().strftime("%Y%m%d")))
    description = "The set of hit calls from the toxcast assay category/subcategory: {} taken on the date:{}"\
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
if __name__ == "__main__":

    #QUERY MC5 data for hitcalls, chemical IDs, assay subcategories
    mysession = SQLSession(Schemas.information_schema).get_session()

    query0 = mysession.query(Compounds.id, Compounds.dsstox_compound_id, Mc5.hitc, Mc5.aeid, AssayComponentEndpoint.assay_component_endpoint_name, AssayComponent.assay_component_desc, AssayComponent.assay_component_target_desc, AssayComponentEndpoint.assay_component_endpoint_desc, AssayComponentEndpoint.assay_function_type, AssayComponentEndpoint.normalized_data_type, AssayComponentEndpoint.analysis_direction, AssayComponentEndpoint.burst_assay, AssayComponentEndpoint.key_positive_control, AssayComponentEndpoint.signal_direction, AssayComponentEndpoint.intended_target_type, AssayComponentEndpoint.intended_target_type_sub, AssayComponentEndpoint.intended_target_family, AssayComponentEndpoint.intended_target_family_sub, AssayComponent.assay_design_type, AssayComponent.assay_design_type_sub, AssayComponent.biological_process_target, AssayComponent.detection_technology_type, AssayComponent.detection_technology_type_sub, AssayComponent.detection_technology, AssayComponent.signal_direction_type, AssayComponent.key_assay_reagent, AssayComponent.key_assay_reagent_type, AssayComponent.technological_target_type, AssayComponent.technological_target_type_sub) \
        .join(GenericSubstanceCompounds, Compounds.id == GenericSubstanceCompounds.fk_compound_id) \
        .join(GenericSubstances, GenericSubstances.id == GenericSubstanceCompounds.fk_generic_substance_id) \
        .join(Sample, Sample.chid == GenericSubstances.id) \
        .join(Mc4, Mc4.spid == Sample.spid) \
        .join(Mc5, Mc5.m4id == Mc4.m4id) \
        .join(AssayComponentEndpoint, AssayComponentEndpoint.aeid == Mc5.aeid) \
        .join(AssayComponent, AssayComponent.acid == AssayComponentEndpoint.acid)

    mytable = pd.DataFrame(list(query0))

    ####################################################################################################################

    ### MAKE TABLES FOR SUBCATEGORIES ###

    #loop through characteristics
    for x in mytable.columns[9:]:
        for y in mytable[x].unique():
            if pd.isnull(y) == True:
                #print('\nnull/nan value found!\n')
                #print(y)
                continue

            #create subcat table
            #may need to remove extra columns
            subcat_table = mytable[mytable[x] == y]

            #format category names
            catname = str(x).replace('/', '-')
            subcatname = str(y).replace('/', '-')

            # naming conventions may change here
            aeid_query = mysession.query(Datasets.name) \
                .filter(Datasets.name.like("assay_cat:{}/_{}/_%".format(catname, subcatname), escape='/'))
            aeid_query = list(aeid_query)
            aeid_query = [x[0] for x in aeid_query]

            # create dataset if one does not exist
            if aeid_query == [] or aeid_query==[''] or aeid_query==None:
                print("New AEID, filling mysql database for assay_cat:{}_{}".format(catname, subcatname))
                assay_name = "{}_{}".format(catname, subcatname)
                filldatasets(subcat_table, assay_name)

            else:
                # find and retrieve the newest dataset name
                aeid_query_dates = [x.split('_')[-1] for x in aeid_query]
                newest_aeid_date = sorted(aeid_query_dates)[0]
                newest_aeid = [x for x in aeid_query if str(newest_aeid_date) in x]

                #pull table and compare
                old_df = mysession.query(Datapoints.efk_dsstox_compound_id, Datapoints.measured_value_dn)\
                    .join(DatasetDatapoints, Datapoints.id==DatasetDatapoints.fk_datapoint_id)\
                    .join(Datasets, DatasetDatapoints.fk_dataset_id==Datasets.id)\
                    .filter(Datasets.name==newest_aeid[0])

                old_df = pd.DataFrame(list(old_df))


                #format datatables for comparison
                ##FORMAT DFs FOR COMPARING
                #rename columns
                old_df.columns = ['id', 'hitc']
                my_new_df = subcat_table.loc[:,['id', 'hitc']]
                old_df['hitc'] = old_df['hitc'].astype(int)

                #sort dataframes
                my_new_df = my_new_df.sort_values(['id', 'hitc'])
                old_df = old_df.sort_values(['id', 'hitc'])

                #reset index
                my_new_df = my_new_df.reset_index(drop=True)
                old_df = old_df.reset_index(drop=True)

                #perform the comparison of datatables
                if my_new_df.equals(old_df)==True:
                    print("no change for assay_cat:{}_{}".format(catname, subcatname))
                    pass

                else:
                    print("Update, filling mysql database for assay_cat:{}_{}".format(catname, subcatname))
                    filldatasets(subcat_table, assay_name)


####################################################################################################################