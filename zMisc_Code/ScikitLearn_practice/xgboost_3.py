import numpy as np
import csv
import sys
import math
import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_score
import inspect

# import dataset
dataset1 = pd.read_csv('/home/rlougee/Desktop/aeid_100_invitrodbv2_fp.tsv', delimiter='\t')
print(dataset1.head())

dataset = dataset1.iloc[:,1:].as_matrix()

# cross validation
x = dataset[:,1:]
y = dataset[:,0]
# use statified k fold cv due to imbalanced data
kfold = StratifiedKFold(n_splits=10)#, random_state=7)
# kfold = KFold(n_splits=10)

# make the model
# booster:  gbtree vs dart makes no noticeable difference

model = xgb.XGBClassifier(booster='gbtree', num_boost_round=20000, max_depth=14, silent=1, max_delta_step=0, learning_rate=0.35, min_child_weight=3, subsample=1) # gamma
results = cross_val_score(model, x, y, cv=kfold)
print("Accuracy: {}({})".format(round(results.mean()*100,3), round(results.std()*100,3)))
print(results)



#visualization
model.fit(x,y)
# xgb.train(x
# print(x.view())
# print(dataset.dtype.names)
# X_columns = x.dtype.names
# print(X_columns)
print(list(zip(dataset1.columns[2:], model.feature_importances_)))
xgb.plot_tree(model, rankdir='LR')
xgb.plot_importance(model, importance_type="weight") #importance type (weight, gain, cover)
plt.tight_layout()
plt.show()
