import numpy as np
import csv
import sys
import math
import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.model_selection import cross_val_score
import inspect

# MAKE A HIERARCHICAL CROSS VALIDATION FUNCTION FOR XGBOOST

# import dataset
dataset = pd.read_csv('/home/rlougee/Desktop/invitrodb_v2_enrichments/CTEW_aeid_100_invitrodbv2_20180918/CTEW_Results/CT-Enriched_FP_aeid_100_invitrodbv2_20180918.tsv', delimiter='\t')
dataset = dataset.iloc[:,1:].as_matrix()

# cross validation
x = dataset[:,1:]
y = dataset[:,0]

print(dataset)

dtrain = xgb.DMatrix(dataset)
param = {'max_depth':2, 'eta':1, 'silent':1, 'objective':'binary:logistic'}
num_round=2

xgb.cv(param, dtrain, num_round, nfold=10)


