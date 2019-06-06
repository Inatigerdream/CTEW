import pandas as pd
import sys

# This Code will simply split our master invitrodb_v3_1 file into smaller datatables by AEID

a = pd.read_csv('/home/rlougee/Desktop/invitrodb_v3_1_data/INVITRODB_V3_1_HITCALLS_BURST_AND_BASELINE_2019.tsv', sep='\t')

print(a.head())
print(a.columns)

# sys.exit(0)
for i in a['aeid'].unique():
    b = a[a['aeid']==i]
    # c = b[['dsstox_compound_id','Baseline Hit Call']]
    d = b[['dsstox_compound_id', 'Burst Filtered Hit Call']]

    # c.to_csv('/home/rlougee/Desktop/invitrodb_v3_1_data/baseline_hitc/AEID:{}_invitrodb_v3_1_baseline_hitc_MC.tsv'.format(i), sep='\t', index=False, header=False)
    d.to_csv('/home/rlougee/Desktop/invitrodb_v3_1_data/burst_hitc/AEID:{}_invitrodb_v3_1_burst_hitc_MC.tsv'.format(i), sep='\t', index=False, header=False)