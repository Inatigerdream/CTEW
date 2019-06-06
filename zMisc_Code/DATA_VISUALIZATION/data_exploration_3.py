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

# which fingerprint set do we want?
# dsi is descriptor set index
dsi = 1445
# 1445 = toxprints
# 1446 = MACCS
# 1447 = pubchem

### I WANT TO SEE THE TOTAL PREVELANCE FOR CHEMOTYPES ACROSS THE ENTIRE ASSAY SPACE ###

## Get matrix containing DTXCIDS, fingerprints

mysession1 = SQLSession(Schemas.dsstox_schema).get_session()

query2 = mysession1.query(Compounds.dsstox_compound_id, CompoundDescriptorSets.descriptor_string_tsv) \
    .join(CompoundDescriptorSets, Compounds.id == CompoundDescriptorSets.efk_dsstox_compound_id) \
    .filter(CompoundDescriptorSets.fk_descriptor_set_id == dsi)

df2 = pd.DataFrame(list(query2))

# something to separate and name fingerprint columns
df2 = pd.concat([df2, df2['descriptor_string_tsv'].str[:].str.split('\t', expand=True)], axis=1)
df2 = df2.drop('descriptor_string_tsv', axis=1)
# print(df2)

# name the columns correctly
query3 = mysession1.query(Descriptors.descriptors_name).filter(Descriptors.fk_descriptor_set_id == dsi)
descriptornames = list(query3)

for num, name in enumerate(descriptornames, start=0):
    df2 = df2.rename(columns={num: name[0]})

# # creates the final output table
# mytable = mytable.rename(columns={colname: "dsstox_compound_id"})
# mytable = pd.merge(mytable, df2, on='dsstox_compound_id')
# # mytable = mytable.drop('dsstox_compound_id', 1)
# outputtable = mytable

# check for trailing column created by tab and remove
if df2[df2.columns[-1]][0] == '':
    df2 = df2.drop(df2.columns[-1], axis=1)

# df2.to_csv("~/Desktop/DTXCIDs_fingerprints_full.tsv" , sep='\t', index=False)

print(df2.head())



### I WANT TO SEE THE TOTAL PREVALANCE FOR CHEMOTYPES ACROSS INDIVIDUAL ASSAYS ###

## Get matrix containing DTXCIDS, assay id, fingerprints

# mysession1 = SQLSession(Schemas.dsstox_schema).get_session()
#
# query2 = mysession1.query(Compounds.dsstox_compound_id, CompoundDescriptorSets.descriptor_string_tsv) \
#     .join(CompoundDescriptorSets, Compounds.id == CompoundDescriptorSets.efk_dsstox_compound_id) \
#     .filter(CompoundDescriptorSets.fk_descriptor_set_id == dsi)
#
# df2 = pd.DataFrame(list(query2))
#
# # something to separate and name fingerprint columns
# df2 = pd.concat([df2, df2['descriptor_string_tsv'].str[:].str.split('\t', expand=True)], axis=1)
# df2 = df2.drop('descriptor_string_tsv', axis=1)
# # print(df2)
#
# # name the columns correctly
# query3 = mysession1.query(Descriptors.descriptors_name).filter(Descriptors.fk_descriptor_set_id == dsi)
# descriptornames = list(query3)