import pandas as pd
from database.session import SQLSession
from database.database_schemas import Schemas
from database.information.TABLES import Tables
from database.invitrodb.mc5 import Mc5


# IMPORT AND CLEAN UP DATATABLES

nonburst = pd.read_csv("/home/rlougee/Desktop/primary_data/Non-Burst_MC_v2_2018_full_enrichment_results.tsv", sep='\t')
burst = pd.read_csv("/home/rlougee/Desktop/primary_data/Burst_MC_v2_2018_full_enrichment_results.tsv", sep='\t')

nonburst['name'] = nonburst['name'].str.replace('Imported_DataTable:aeid_','').str.replace('_invitrodbv2_20180918', '').apply(int)
burst['name'] = burst['name'].str.replace('Imported_DataTable:','').str.replace('_Burst_MC_v2_20181120', '')

print(nonburst.tail())
print(burst.tail())

# QUERY AEID AND CORRECT ASSAY NAMES

mysession = SQLSession(Schemas.information_schema).get_session()


q0 = mysession.execute('SELECT aeid, assay_component_endpoint_name FROM sbox_rlougee_invitrodb.assay_component_endpoint')
q0 = pd.DataFrame(list(q0))
# q0[1] = q0[1].apply(str)
print('q0 shape', q0.shape)
print('nonburst shape', nonburst.shape)
print('burst shape', burst.shape)

nonburst2 = pd.merge(nonburst, q0, how='inner', left_on=['name'], right_on=[0])
print(nonburst2.shape)

burst2 = pd.merge(burst, q0, how='inner', left_on=['name'], right_on=[1])
print(burst2.shape)

# ok merges look good now

nonburst2.to_csv('/home/rlougee/Desktop/nonburst.tsv', sep='\t')
burst.to_csv('/home/rlougee/Desktop/burst.tsv', sep='\t')