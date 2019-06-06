import pandas as pd

mytable = pd.read_csv('~/Desktop/aeid_hitcall_SID_table_for_Ann.tsv', sep='\t')

print(mytable.head())

mytable = pd.pivot_table(mytable, values='hitc', index=['id', 'dsstox_compound_id'], columns=['aeid'])

print(mytable)

# mytable.to_csv("~/Desktop/Anns_table.tsv", sep='\t')