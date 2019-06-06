import numpy as np
import pandas as pd
import random
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV

hit30 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/DIO1_PhII-hit30_JOlker_fp.tsv', sep='\t', index_col=0)
hit50 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/DIO1_PhII-hit50_JOlker_fp.tsv', sep='\t', index_col=0)

# hit30 = hit30.sort_values('hitcall.30', ascending=False)
# hit50 = hit50.sort_values('hitcall.50', ascending=False)

# typical way to split into test and training sets
# X_, X_test, y_, y_test = train_test_split(hit30.iloc[:,1],hit30.iloc[:,2:], test_size=0.2, stratify=hit30.iloc[:,1])

y50 = hit50.iloc[:,0]
# x50 = hit50.iloc[:,1:]

y30 = hit30.iloc[:,0]
# x50 = hit50.iloc[:,1:]

# print(y50.value_counts())
print(hit30.head(0))
print(y30.value_counts())
print(y50.value_counts())

# separate rows with positive hits

hit30pos = hit30[hit30['hitcall.30'] == 1]
hit30neg = hit30[hit30['hitcall.30'] == 0]

print('\n', hit30.shape, hit30pos.shape, hit30neg.shape)

# randomly select 120 rows from hit30 pos
def random_select(df, num_rows):
    return df.ix[random.sample(list(df.index), num_rows)]

a = random_select(hit30pos, 120)
b = random_select(hit30pos, 120)
c = random_select(hit30pos, 120)
d = random_select(hit30pos, 120)
e = random_select(hit30pos, 120)

print(hit50.shape, a.append(hit30neg).shape)

a.append(hit30neg).to_csv('/share/home/rlougee/Desktop/JOlker_split_a.tsv', sep='\t', index=True)
b.append(hit30neg).to_csv('/share/home/rlougee/Desktop/JOlker_split_b.tsv', sep='\t', index=True)
c.append(hit30neg).to_csv('/share/home/rlougee/Desktop/JOlker_split_c.tsv', sep='\t', index=True)
d.append(hit30neg).to_csv('/share/home/rlougee/Desktop/JOlker_split_d.tsv', sep='\t', index=True)
e.append(hit30neg).to_csv('/share/home/rlougee/Desktop/JOlker_split_e.tsv', sep='\t', index=True)

