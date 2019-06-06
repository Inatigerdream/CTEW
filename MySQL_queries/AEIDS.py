from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.qsar.compound_descriptors import CompoundDescriptors
from database.session import SQLSession
from database.dsstox.generic_substance_compounds import GenericSubstanceCompounds
from database.dsstox.generic_substances import GenericSubstances
from database.qsar.datasets import Datasets
from database.qsar.dataset_datapoints import DatasetDatapoints
from database.qsar.datapoints import Datapoints
from database.qsar.univariate_calculations import UnivariateCalculations
from sqlalchemy import or_, and_, any_

import pandas as pd

# mytable = pd.read_csv('~/Desktop/mc5_clean.tsv', sep='\t')
#
# print(mytable.tail())

mysession = SQLSession(Schemas.information_schema).get_session()
#
# query1 = mysession.query(Datapoints.efk_dsstox_compound_id, Datapoints.measured_value_dn, Datasets.name) \
#     .join(DatasetDatapoints, Datapoints.id == DatasetDatapoints.fk_datapoint_id) \
#     .join(Datasets, DatasetDatapoints.fk_dataset_id == Datasets.id)
#
# query1 = pd.DataFrame(list(query1))
# print(query1.head())
#
# print([x.split('_',1)[0][5:] for x in query1.name.unique()])

x_aeid = 'aeid:926_20171128'

# my_enrichment_date = mysession.query(UnivariateCalculations.updated_at, Datasets.id)\
#         .join(Datasets, Datasets.id==UnivariateCalculations.fk_dataset_id)\
#         .filter(Datasets.name==x_aeid)
#
# my_enrichment_date =str(list(my_enrichment_date)[0][0])
# my_enrichment_date = my_enrichment_date.split(' ', 1)[0]
# print(my_enrichment_date)
# my_enrichment_date_list = my_enrichment_date.split('-', 2)
# print(my_enrichment_date_list)
# my_enrichment_date = my_enrichment_date_list[0] + my_enrichment_date_list[1] + my_enrichment_date_list[2]
# print(my_enrichment_date)

# query2 = mysession.query(UnivariateCalculations.fk_dataset_id)
#
# query2 = pd.DataFrame(list(query2))
# print(query2.fk_dataset_id.unique()[0])

query0 = mysession.query(UnivariateCalculations.fk_dataset_id)
query0 = pd.DataFrame(list(query0))
query0 = query0.fk_dataset_id.unique()
# query0 = [str(x) for x in query0]

print('step1')

query1 = mysession.query(Datapoints.efk_dsstox_compound_id, Datapoints.measured_value_dn, Datasets.name, Datasets.id) \
        .join(DatasetDatapoints, Datapoints.id == DatasetDatapoints.fk_datapoint_id) \
        .join(Datasets, DatasetDatapoints.fk_dataset_id == Datasets.id)

query1 = pd.DataFrame(list(query1))
query1 = query1[~query1['id'].isin(query0)]


print(query1.head())



# dtxsid = mytable.iloc[:,4]
#
# mysession = SQLSession(Schemas.qsar_schema).get_session()
#
# query = mysession.query(GenericSubstances.dsstox_substance_id, Compounds.id, Compounds.dsstox_compound_id).join(
#     GenericSubstanceCompounds) \
#     .join(Compounds).filter(GenericSubstances.dsstox_substance_id.in_(dtxsid))
#
# df = pd.DataFrame(list(query))
#
# myids = [int(x) for x in df.iloc[:,1]]
#
# # query1 = mysession.query(Compounds.id, Compounds.dsstox_compound_id).filter(Compounds.dsstox_compound_id.in_(dtxsid))
# # df1 = pd.DataFrame(list(query1))
#
# query2 = mysession.query(CompoundDescriptors.efk_dsstox_compound_id, CompoundDescriptors.descriptor_string_tsv,
#                          CompoundDescriptors.fk_descriptor_set_id).filter(
#     CompoundDescriptors.efk_dsstox_compound_id.in_(myids))
# df2 = pd.DataFrame(list(query2))
#
# df2 = df2.rename(columns={"efk_dsstox_compound_id":'id'})
# mytable2 = pd.merge(df, df2, on='id')
# mytable2 = mytable2.rename(columns={"dsstox_substance_id":'DTXSID'})
# mytable3 = pd.merge(mytable, mytable2, on='DTXSID')
#
#
# mytable3.to_csv("~/Desktop/Katies_data_full" , sep='\t')
