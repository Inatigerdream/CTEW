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
import re


# FIRST NEED TO GET A TABLE index = AEID and columns = Assay Cats, Toxprints Enrichments (discrete hitcalls for each assay)
# going to do this in two parts
# part 1 get assay cats X aeids
mysession = SQLSession(Schemas.information_schema).get_session()

query0 = mysession.query(AssayComponentEndpoint.aeid,
                         AssayComponentEndpoint.assay_component_endpoint_name, AssayComponent.assay_component_desc,
                         AssayComponent.assay_component_target_desc,
                         AssayComponentEndpoint.assay_component_endpoint_desc,
                         AssayComponentEndpoint.assay_function_type, AssayComponentEndpoint.normalized_data_type,
                         AssayComponentEndpoint.analysis_direction, AssayComponentEndpoint.burst_assay,
                         AssayComponentEndpoint.key_positive_control, AssayComponentEndpoint.signal_direction,
                         AssayComponentEndpoint.intended_target_type, AssayComponentEndpoint.intended_target_type_sub,
                         AssayComponentEndpoint.intended_target_family,
                         AssayComponentEndpoint.intended_target_family_sub, AssayComponent.assay_design_type,
                         AssayComponent.assay_design_type_sub, AssayComponent.biological_process_target,
                         AssayComponent.detection_technology_type, AssayComponent.detection_technology_type_sub,
                         AssayComponent.detection_technology, AssayComponent.signal_direction_type,
                         AssayComponent.key_assay_reagent, AssayComponent.key_assay_reagent_type,
                         AssayComponent.technological_target_type, AssayComponent.technological_target_type_sub) \
    .join(AssayComponent, AssayComponent.acid == AssayComponentEndpoint.acid)

mytable = pd.DataFrame(list(query0))

mytable.to_csv("~/Desktop/Assay_Categories/assay_cats_x_aeids_v2.tsv" , sep='\t')

sys.exit(0)

mytable = pd.read_csv("~/Desktop/Assay_Categories/assay_cats_x_aeids.tsv" , sep='\t')
print(mytable)


# part 2 get Discrete Toxprint Enrichments x aeids
# import separately?

# mytable2 = pd.read_csv("~/Desktop/Assay_Categories/FULL_TXP_OR_PVAL.tsv" , sep='\t')
# print(mytable2.columns.values)
# mytable2 = mytable2.drop(['label', 'Inv OR', 'Inv P-val'], axis=1)
# mytable3 = mytable2.pivot(index='name', columns='descriptors_name')
# print(mytable3.columns.values)
# print(mytable3.index.values)
# mytable3[('aeid','')] = 0
# for i in mytable3.index.values:
#     mytable3.loc[i, ('aeid','')] = i.split(':')[1].split('_')[0]
#     print(mytable3.loc[i, 'aeid'])

# print(mytable3.head())


# mytable3.to_csv("~/Desktop/Assay_Categories/FULL_TXP_OR_PVAL2.tsv" , sep='\t')




# mytable3 = pd.read_csv("~/Desktop/Assay_Categories/FULL_TXP_OR_PVAL2.tsv" , sep='\t')
# mytable3 = mytable3.drop([1])
#
# # make a final datatable
#
# columns = ['aeid']
# for i, row in mytable3.iterrows():
#     # print(row.index)
#     columns.extend(list(row[1:730]))
#     break
#
# final_table = pd.DataFrame(columns=columns, index=range(1575))
# for i in range(len(mytable3.iloc[1:,1459])):
#     final_table.iloc[i, 0] = int(mytable3.iloc[i+1, 1459])
#
# print(final_table)
#
# # fill final table
# # print(mytable3.head())
# mytable3 = mytable3.drop([0])
# for idx, row in mytable3.iterrows():
#     # print(row[1], row[730])
#     # print(row[0])
#     # print(row)
#     for num in range(729):
#         # try:
#         #     print(row[num+1], row.loc['OR.{}'.format(num)], row[num+730], row.loc['P-Val.{}'.format(num)])
#         # except:
#         #     None
#         if float(row[num+1]) >= 3 and float(row[num + 730]) <= 0.05:
#             final_table.iloc[idx-2 ,num+1] = 1
#             # print('add')
#         else:
#             final_table.iloc[idx-2 ,num+1] = 0
#             # print('daa')
#     # print(final_table.head())
#     # print(row)
#
# print(final_table)
# final_table.to_csv("~/Desktop/Assay_Categories/Enriched_Chemotype_Matrix_x_aeid2.tsv" , sep='\t')








# mytable4 = pd.read_csv("~/Desktop/Assay_Categories/Enriched_Chemotype_Matrix_x_aeid2.tsv" , sep='\t')
#
# mytable4 = mytable4.drop(['Unnamed: 0'], axis=1)
# mytable = mytable.drop(['Unnamed: 0'], axis=1)
#
# # join tables on aeid
# master_table = pd.merge(mytable, mytable4, how='inner', on=['aeid'])
# master_table.to_csv("~/Desktop/Assay_Categories/Master_table_aeidXcatsXenrich.tsv" , sep='\t')








master_table = pd.read_csv("~/Desktop/Assay_Categories/Master_table_aeidXcatsXenrich.tsv" , sep='\t')
master_table = master_table.drop(['Unnamed: 0', 'assay_component_endpoint_name', 'assay_component_desc', 'assay_component_target_desc', 'assay_component_endpoint_desc'], axis=1)
master_table = master_table.set_index('aeid', drop=True)
# print(master_table.head())

# make datasets for each assay category
# loop through characteristics
for i, x in enumerate(master_table.columns[:21]):
    print(i,x)

    for idx, y in enumerate(master_table[x].unique()):
        if pd.isnull(y) == True:
            continue

        print('\t', idx, y)
        #make a tabel for subcat
        subcat = master_table.iloc[:,21:]
        #add hitcall column
        subcat.insert(0, 'hitc', 0)
        for aeid in master_table[master_table[x] == y].index:
            subcat.loc[aeid,'hitc'] = 1
        #format assay names
        pattern = re.sub('[\W_]+', '', str(y))
        #write table to dir
        subcat.to_csv("~/Desktop/Assay_Categories/data_tables/{}_{}_table.tsv".format(x,pattern) , sep='\t')


        # create subcat table
        # may need to remove extra columns
    #     subcat_table = master_table[master_table[x] == y]
    # print(subcat_table.head())





# print(subcat.head())
# print(master_table.iloc[:,0:25])
# print(mytable.head())
