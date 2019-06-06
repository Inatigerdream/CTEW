import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV

hit1 = pd.read_csv('/home/rlougee/Desktop/JUN_CV/NIS_ph1,2_hit1_rev4.tsv', sep='\t', index_col=0)
hit2 = pd.read_csv('/home/rlougee/Desktop/JUN_CV/NIS_ph1,2_v2_hitcall2_rev3.tsv', sep='\t', index_col=0)

y2 = hit2.iloc[:,0]
# x50 = hit50.iloc[:,1:]

y1 = hit1.iloc[:,0]
# x50 = hit50.iloc[:,1:]

# print(y50.value_counts())
print(hit1.head(0))
print(y1.value_counts())
print(y2.value_counts())

# separate rows with positive hits

hit1pos = hit1[hit1['Hit-1 (273)'] == 1]
hit1neg = hit1[hit1['Hit-1 (273)'] == 0]

print('\n', hit1.shape, hit1pos.shape, hit1neg.shape)

# randomly select 120 rows from hit30 pos
def random_select(df, num_rows):
    return df.ix[random.sample(list(df.index), num_rows)]

a = random_select(hit1pos, 63)
b = random_select(hit1pos, 63)
c = random_select(hit1pos, 63)
d = random_select(hit1pos, 63)
e = random_select(hit1pos, 63)

print(hit2.shape, a.append(hit1neg).shape)

a.append(hit1neg).to_csv('/share/home/rlougee/Desktop/JUN_CV_split_a.tsv', sep='\t', index=True)
b.append(hit1neg).to_csv('/share/home/rlougee/Desktop/JUN_CV_split_b.tsv', sep='\t', index=True)
c.append(hit1neg).to_csv('/share/home/rlougee/Desktop/JUN_CV_split_c.tsv', sep='\t', index=True)
d.append(hit1neg).to_csv('/share/home/rlougee/Desktop/JUN_CV_split_d.tsv', sep='\t', index=True)
e.append(hit1neg).to_csv('/share/home/rlougee/Desktop/JUN_CV_split_e.tsv', sep='\t', index=True)

