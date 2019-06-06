import datetime
import math
from database.session import SQLSession
from database.database_schemas import Schemas
from database.information.TABLES import Tables
from database.invitrodb.mc5 import Mc5
from database.invitrodb.assay_component_endpoint import AssayComponentEndpoint
from database.invitrodb.assay_component import AssayComponent
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
from sqlalchemy import or_, and_
import sys
import pandas as pd
from io import StringIO



# ### PULL A FULL AEID TABLE ###
# mysession = SQLSession(Schemas.information_schema).get_session()
#
# query0 = mysession.query(Compounds.id, Compounds.dsstox_compound_id, Mc5.hitc, Mc5.aeid, AssayComponentEndpoint.assay_component_endpoint_name, AssayComponent.assay_component_desc, AssayComponent.assay_component_target_desc, AssayComponentEndpoint.assay_component_endpoint_desc, AssayComponentEndpoint.assay_function_type, AssayComponentEndpoint.normalized_data_type, AssayComponentEndpoint.analysis_direction, AssayComponentEndpoint.burst_assay, AssayComponentEndpoint.key_positive_control, AssayComponentEndpoint.signal_direction, AssayComponentEndpoint.intended_target_type, AssayComponentEndpoint.intended_target_type_sub, AssayComponentEndpoint.intended_target_family, AssayComponentEndpoint.intended_target_family_sub, AssayComponent.assay_design_type, AssayComponent.assay_design_type_sub, AssayComponent.biological_process_target, AssayComponent.detection_technology_type, AssayComponent.detection_technology_type_sub, AssayComponent.detection_technology, AssayComponent.signal_direction_type, AssayComponent.key_assay_reagent, AssayComponent.key_assay_reagent_type, AssayComponent.technological_target_type, AssayComponent.technological_target_type_sub) \
#     .join(GenericSubstanceCompounds, Compounds.id == GenericSubstanceCompounds.fk_compound_id) \
#     .join(GenericSubstances, GenericSubstances.id == GenericSubstanceCompounds.fk_generic_substance_id) \
#     .join(Sample, Sample.chid == GenericSubstances.id) \
#     .join(Mc4, Mc4.spid == Sample.spid) \
#     .join(Mc5, Mc5.m4id == Mc4.m4id) \
#     .join(AssayComponentEndpoint, AssayComponentEndpoint.aeid == Mc5.aeid) \
#     .join(AssayComponent, AssayComponent.acid == AssayComponentEndpoint.acid)
#
# AEID_table = pd.DataFrame(list(query0))
#
# print("########################")
# print(AEID_table.head())
# print("########################")
# print(AEID_table.columns)
# print("########################")
# print(AEID_table.shape)
# print("########################")
#
#
# ### EXPORT TABLE ###
#
# AEID_table.to_csv("~/Desktop/AEID_fulldump_with_CATS.tsv" , sep='\t')

### IMPORT TABLE ###
mytable = pd.read_csv('~/Desktop/AEID_fulldump_with_CAT.tsv', sep='\t')
# print(mytable.head())

# print columns
print(mytable.columns)

# ### GENERATE A TABLE W/ GENERAL STATISTICS ###
# # make a dataframe
# my_df = pd.DataFrame(columns=['characteristic', 'subcharacteristic', 'total_hits', 'total_rows', 'percentage_hits', 'assay_count', 'assay_list', 'assay_names'])
#
# #characteristic list
# char_list = []
# sub_char_list = []
#
# #loop through characteristics, generate statistics
# count = 0
# for x in mytable.columns[9:]:
#     for y in mytable[x].unique():
#         if pd.isnull(y) == True:
#             print('\nnull/nan value found!\n')
#             print(y)
#             continue
#         a = mytable[ mytable[x] == y ]
#         print('###############')
#         print('characteristic: ', x)
#         my_df.loc[count, 'characteristic'] = x
#         print('subcharacteristic: ', y)
#         my_df.loc[count, 'subcharacteristic'] = y
#         print('assay_count: ', len(a.loc[:,'aeid'].unique()))
#         my_df.loc[count, 'assay_count' ] = len(a.loc[:,'aeid'].unique())
#         my_df.loc[count, 'assay_list'] = a.loc[:,'aeid'].unique()
#         my_df.loc[count, 'assay_names'] = a.loc[:,'assay_component_endpoint_name'].unique()
#         print('total hits: ', sum(a['hitc']))
#         my_df.loc[count, 'total_hits'] = sum(a['hitc'])
#         print('total rows: ', a.shape[0])
#         my_df.loc[count, 'total_rows'] = a.shape[0]
#         print( 'percentage hits: ', round(sum(a['hitc'])/a.shape[0]*100, 1),'%')
#         my_df.loc[count, 'percentage_hits'] = round(sum(a['hitc'])/a.shape[0]*100, 1)
#         count+=1
#         char_list.append(x)
#         sub_char_list.append(str(y))
#
#
#
# print(my_df)
# # my_df.to_csv("~/Desktop/Assay_characteristic_breakdown_v3.tsv" , sep='\t')
# print('#######################################')
# print('characteristics count: ', len(set(char_list)))
# print(list(set(char_list)))
# print('#######################################')
# print('sub_characteristics count: ', len(sub_char_list))
# print(sub_char_list)
# print('#######################################')


### GENERATE DATATABLES FOR CHARACTERISTICS/SUBCHARACTERISTICS ###
for i in set(mytable.columns[9:]):
    b = mytable[mytable[i].notnull()]
    #print each tables shape
    print(i, b.shape)

    for j in b[i].unique():
        # print sbb = b[['dsstox_compound_id', 'hitc']]ubcategories
        c = b[b[i] == j]
        bb = c[['dsstox_compound_id', 'hitc']]
        print('\t', j, bb.shape)
        i = str(i).replace('/', '-')
        j = str(j).replace('/', '-')
        bb.to_csv("~/Desktop/subcat_matrices/data_tables/{}_{}.tsv".format(str(i), str(j)) , sep='\t', index=False)








