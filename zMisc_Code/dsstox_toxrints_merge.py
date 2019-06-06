import pandas as pd
import sys
full = pd.read_csv('/home/rlougee/Desktop/DSSTox_TSCAACTIVE_CID.tsv', sep='\t', names= ['dsstox_compound_id'])
txp = pd.read_csv('/home/rlougee/Desktop/DSSTox_TSCAACTIVE_CID_TXP.tsv', sep='\t')

# print(pd.DataFrame(full).head())
# txp = txp.dropna(axis=1)
# txp = txp['dsstox_compound_id']

# sys.exit(0)
print(list(set(full['dsstox_compound_id']) - set(txp['dsstox_compound_id'])))