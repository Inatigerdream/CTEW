import pandas as pd

# this looks like how enriched a chemotype is in an assay cat vs all assays

df1 = pd.read_csv('~/Desktop/Assay_Categories/global_CT_frequencies/Percent_Enriched_Assays_Toxprints2.tsv', sep='\t', header=None)

df1.columns = ['Fingerprint_ID', 'Percent_Enriched']

df2 = pd.read_csv('/home/rlougee/Desktop/Assay_Categories/enrichment_tables/intended_target_family_nuclearreceptor_table.tsv', sep='\t')

df2['Percent_Enriched'] = df2['TP']/15.75
df2 = df2.drop(['F-Total', 'TP', 'FP', 'FN', 'TN', 'Balanced Accuracy'], axis=1)

print(df1.columns, df2.columns)



df3 = pd.merge(df2, df1, how='inner', on='Fingerprint_ID')

# print(df1)
# print(df2)
print(df3)