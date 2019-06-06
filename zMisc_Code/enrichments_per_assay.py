import pandas as pd

#import all AEID enrichment data
df1 = pd.read_csv('/home/rlougee/Desktop/ALL_AEID_ENRICHMENT_DATA.tsv', sep='\t')

#get full table info
print(df1.head())
print('\n', df1.shape)

# set statistical thresholds for significance
df = df1[df1['TP'] > 5]
print(df.shape)
df = df[df['OR'] >= 3.0]
print(df.shape)
df = df[df['P-Val'] <= 0.05]
print(df.shape)

# how many enriched per assay?
num_enriched = df['name'].value_counts()
print('AEID_COUNT:', len(df1['name'].unique()), len(num_enriched.index.unique()),'AEID > 30', len([x for x in num_enriched if x > 30]), 'AEID < 5',len([x for x in num_enriched if x < 5]), 'MAX:', max(num_enriched), 'AVG:', sum(num_enriched)/float(len(num_enriched)))
# print('\n', num_enriched)

