import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV


hit30 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/DIO1_PhII-hit30_JOlker_fp.tsv', sep='\t', index_col=0)
hit50 = pd.read_csv('/home/rlougee/Desktop/JOLKER_files/DIO1_PhII-hit50_JOlker_fp.tsv', sep='\t', index_col=0)

# hit30 = hit30.sort_values('hitcall.30', ascending=False)
# hit50 = hit50.sort_values('hitcall.50', ascending=False)

# typical way to split into test and training sets
# X_, X_test, y_, y_test = train_test_split(hit30.iloc[:,1],hit30.iloc[:,2:], test_size=0.2, stratify=hit30.iloc[:,1])

y = hit50.iloc[:,0]
X = hit50.iloc[:,1:]
# print(y.value_counts())

skf = StratifiedKFold(n_splits=5, shuffle=False)
skf.get_n_splits(X, y)
count=0
for train_index, test_index in skf.split(X, y):
    count +=1
    # print("TRAIN:", len(train_index), "TEST:", test_index)
    y_train, y_test = y[train_index], y[test_index]
    # print(y_test.value_counts())
    X_train, X_test = X.iloc[train_index, :], X.iloc[test_index, :]
    y_train = pd.DataFrame(y_train)
    # print(X_test.index, y_test.index)
    y_train.merge(X_train, how='inner', left_index=True, right_index=True).to_csv('/home/rlougee/Desktop/JOLKER_hit30_train_split_{}.tsv'.format(count), sep='\t')
    y_test = pd.DataFrame(y_test)
    y_test.merge(X_test, how='inner', left_index=True, right_index=True).to_csv('/home/rlougee/Desktop/JOLKER_hit30_test_split_{}.tsv'.format(count), sep='\t')