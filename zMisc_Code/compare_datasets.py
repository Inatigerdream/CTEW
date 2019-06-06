#compare complete toxprint enrichments with kconnors toxprint enrichments

import pandas as pd
import re

mytable = pd.read_csv('~/Desktop/chemotype.invitrodb.v2.160504.csv')

mytable = mytable.drop(['OR95CI.low','OR95CI.high','ORpval','Yules.Q', 'db.vers', 'active.chnm'], axis=1)

mytable.columns = ['assay_component_endpoint_name', 'label', 'aeid', 'CT-Tot', 'TP', 'P-Val', 'OR']

mytable2 = pd.read_csv('~/Desktop/FULL_TP_ENRICHMENTS.tsv', sep='\t')

mytable2 = mytable2.drop(['descriptors_name', 'FN', 'FP', 'TN', 'BA', 'Inv OR', 'Inv P-val'], axis=1)

mytable2['label'] = [re.sub( r'\W+','.', str(x)) for x in mytable2['label']]

mytable3 = pd.merge(mytable, mytable2, how='inner', on=['label', 'assay_component_endpoint_name'])# left_on=aa[3], right_on=bb[1])
mytable4 = pd.merge(mytable2, mytable, how='outer',indicator=True, on=['label', 'assay_component_endpoint_name'])
mytable4 = mytable4[mytable4['_merge'] == 'right_only']



# mytable3 = pd.merge(mytable, mytable2, how='inner', on=['aenm'])
print('kconnors:')
print(mytable.shape)
print(mytable.columns)
# print(mytable)
print('###################')
print('rlougee:')
print(mytable2.shape)
print(mytable2.columns)
# print(mytable2)
print('###################')
print('innerjoin')
print(mytable3.shape)
# print(mytable3)
print('####################')
print('diff / right join')
print(mytable4.shape)

print(len(mytable4['assay_component_endpoint_name'].unique()))

print(mytable4['label'].unique())
print(mytable2['label'].unique())

# mytable4.to_csv("~/Desktop/KC_RL_nonmerge_v1.tsv" , sep='\t')

