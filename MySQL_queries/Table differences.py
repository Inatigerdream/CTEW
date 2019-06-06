from database.database_schemas import Schemas
from database.invitrodb.mc5 import Mc5
from database.invitrodb.mc4 import Mc4
from database.invitrodb.sample import Sample
from database.dsstox.compounds import Compounds
from database.dsstox.generic_substances import GenericSubstances
from database.dsstox.generic_substance_compounds import GenericSubstanceCompounds
from database.session import SQLSession

import pandas as pd


########################################################################################################################

mysession = SQLSession(Schemas.information_schema).get_session()

query0 = mysession.query(Mc5.aeid, Mc5.hitc, Sample.spid) \
    .join(Mc4, Mc5.m4id == Mc4.m4id) \
    .join(Sample, Mc4.spid == Sample.spid) \
    .join(GenericSubstances, Sample.chid == GenericSubstances.id) \
    .join(GenericSubstanceCompounds, GenericSubstances.id == GenericSubstanceCompounds.fk_generic_substance_id) \
    .join(Compounds, Compounds.id == GenericSubstanceCompounds.fk_compound_id)
mc5_table = pd.DataFrame(list(query0))

########################################################################################################################

mytable1 = pd.read_csv('~/Desktop/tcpl_mc5_dump_v2.tsv', sep='\t')
mytable2= pd.read_csv('~/Desktop/mysql_mc5_dump_v2.tsv', sep='\t')

mytable1 = mytable1.drop(['m5id', 'm4id'], axis=1)
# mytable2 = mytable2.drop(['dsstox_compound_id'], axis=1)


########################################################################################################################

### BUNCH OF CRAP TO GET RID OF QUOTES IN A DATAFRAME ###
# not sure this even works...

# mytable2["'spid'"] = mytable2["'spid'"].translate(str.maketrans({"'":None}))
# mytable2["'spid'"] = map(lambda x:x.replace("'",""), mytable2["'spid'"])
# myspid = mytable2["'spid'"]
# mytable2 = mytable2.ix[:,mytable2.dtypes==object].apply(lambda s:s.str.replace("'",""))
# mytable2 = mytable2.append(myspid)
# mytable2.apply(lambda s:s.replace("'",""))

########################################################################################################################

# print(mytable1.head())
# print(mytable2.head())

aa = list(mytable1)
bb = list(mytable2)

mytable3 = pd.merge(mytable1, mytable2, how='inner', on=['aeid', 'hitc', 'spid'])# left_on=aa[3], right_on=bb[1])
mytable4 = pd.merge(mytable3, mytable1, how='outer',indicator=True, on=['aeid', 'hitc', 'spid'])
mytable4= mytable4[mytable4['_merge'] == 'right_only']
mytable5 = pd.merge(mytable3, mytable2, how='outer',indicator=True, on=['aeid', 'hitc', 'spid'])
mytable5= mytable5[mytable5['_merge'] == 'right_only']
mytable6 = pd.merge(mytable1, mc5_table, how='inner', on=['aeid', 'hitc', 'spid'])
mytable7 = pd.merge(mc5_table, mytable2, how='outer',indicator=True, on=['aeid', 'hitc', 'spid'])
mytable7= mytable7[mytable7['_merge'] == 'right_only']



# print(mytable3.head())

print("tcpl")
print(mytable1.shape)
print("mysql")
print(mytable2.shape)
print("inner join mysql & tcpl")
print(mytable3.shape)
print("tcpl&innerjoin differences")
print(mytable4.shape)
print("mysql&innerjoin differences")
print(mytable5.shape)
print("join between MySQL query and SQLalchemy query")
print(mytable6.shape)
print("difference between MySQL query and SQLalchemy query")
print(mytable7.shape)


mytable4.to_csv("~/Desktop/tcpl_diff_v2.tsv" , sep='\t')
mytable5.to_csv("~/Desktop/mysql_diff_v2.tsv" , sep='\t')
mytable7.to_csv("~/Desktop/mysql_alchemy_diff_v2.tsv" , sep='\t')

