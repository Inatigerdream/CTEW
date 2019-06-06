from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptors import CompoundDescriptors
from database.session import SQLSession
from database.dsstox.generic_substance_compounds import GenericSubstanceCompounds
from database.dsstox.generic_substances import GenericSubstances


import pandas as pd

mytable = pd.read_csv('~/Desktop/Katies_data.tsv', sep='\t')
dtxsid = mytable.iloc[:,4]

mysession = SQLSession(Schemas.qsar_schema).get_session()

query = mysession.query(GenericSubstances.dsstox_substance_id, Compounds.id, Compounds.dsstox_compound_id).join(
    GenericSubstanceCompounds) \
    .join(Compounds).filter(GenericSubstances.dsstox_substance_id.in_(dtxsid))

df = pd.DataFrame(list(query))

myids = [int(x) for x in df.iloc[:,1]]

# query1 = mysession.query(Compounds.id, Compounds.dsstox_compound_id).filter(Compounds.dsstox_compound_id.in_(dtxsid))
# df1 = pd.DataFrame(list(query1))

query2 = mysession.query(CompoundDescriptors.efk_dsstox_compound_id, CompoundDescriptors.descriptor_string_tsv,
                         CompoundDescriptors.fk_descriptor_set_id).filter(
    CompoundDescriptors.efk_dsstox_compound_id.in_(myids))
df2 = pd.DataFrame(list(query2))

df2 = df2.rename(columns={"efk_dsstox_compound_id":'id'})
mytable2 = pd.merge(df, df2, on='id')
mytable2 = mytable2.rename(columns={"dsstox_substance_id":'DTXSID'})
mytable3 = pd.merge(mytable, mytable2, on='DTXSID')
# print(df2.head())
#
# print(mytable.head())

# print(mytable3.head())

mytable3.to_csv("~/Desktop/Katies_data_full" , sep='\t')
