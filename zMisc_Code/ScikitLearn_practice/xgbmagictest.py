import xgbmagic
import pandas as pd
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_score

df = pd.read_csv('/home/rlougee/Desktop/invitrodb_v2_enrichments/CTEW_aeid_100_invitrodbv2_20180918/CTEW_Results/CT-Enriched_FP_aeid_100_invitrodbv2_20180918.tsv', delimiter='\t')
df.iloc[:,2:] = df.iloc[:,2:].astype(int)

for i in df.columns:
    f = i
    f = f.replace('[','')
    f = f.replace(']','')
    f = f.replace('<','')
    if i != f:
        df = df.rename(columns = {i:f})

# classification model = binary
target_type = 'binary'

# set columns type here
xgb = xgbmagic.Xgb(df.iloc[50:,:], target_column='Hit_Call', id_column='Dsstox_Compound_ID', numeric_columns=df.columns[2:])
xgb.train()
print(xgb.feature_importance())
print(xgb.predict(df.iloc[:50,:]))



