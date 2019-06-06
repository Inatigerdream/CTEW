# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import xgboost

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.decomposition import PCA

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import roc_auc_score

import random
#
# random.seed(9001)
#
#
# def Init_GMM_2(n_ind=1000.0, p=[0.05, 0.95]):
#     n_fraude = int(n_ind * p[0])
#     n_ok = int(n_ind - n_fraude)
#
#     colonnes = ['X0', 'X1']
#
#     mean1 = [0, 0]  #
#     cov1 = [[1, 3], [0, 10]]  #
#     data_fraude = pd.DataFrame(np.random.multivariate_normal(mean1, cov1, int(n_fraude / 2)), columns=colonnes)
#     data_fraude['FRAUDE'] = 1
#
#     mean3 = [4, 0]  #
#     cov3 = [[1, 3], [0, 10]]  #
#     data_fraude2 = pd.DataFrame(np.random.multivariate_normal(mean3, cov3, int(n_fraude / 2)), columns=colonnes)
#     data_fraude2['FRAUDE'] = 1
#
#     mean2 = [2, 2]  #
#     cov2 = [[1, 3], [0, 10]]  #
#     data_ok = pd.DataFrame(np.random.multivariate_normal(mean2, cov2, n_ok), columns=colonnes)
#     data_ok['FRAUDE'] = 0
#
#     data = pd.concat([data_fraude, data_ok, data_fraude2])
#     data = data.reset_index(drop=True)
#
#     return data, colonnes, 'FRAUDE'
#
#
# def Nuage(X, feature1, feature2, type_i='FRAUDE'):
#     if type_i not in data.columns:
#         print(type_i, " non disponible")
#         return
#
#     TF = X[X[type_i] == 1]
#     TO = X[X[type_i] == 0]
#
#     plot1 = plt.scatter(TF[feature1], TF[feature2], color='b', marker='x', label='Fraude')
#     plot2 = plt.scatter(TO[feature1], TO[feature2], color='r', marker='.', label='OK')
#
#     plt.legend(handles=[plot1, plot2], loc='best')
#     plt.xlabel(feature1)
#     plt.ylabel(feature2)
#     plt.title(type_i)
#     plt.show()
#
#
# # Creation de la base
# data, predictors, target = Init_GMM_2(n_ind=11000)
#
# # Affichage du nuage de point
# Nuage(data, 'X0', 'X1', target)
#
# # Affichage des caracteristiques de la base
# n0 = len(data[data[target] == 0])
# n1 = len(data[data[target] == 1])
# print("n_fraudes = ", n1)
# print("n_ok = ", n0)

import numpy as np
import xgboost as xgb
from sklearn.model_selection import StratifiedKFold, train_test_split, GridSearchCV

df = pd.read_csv('/home/rlougee/Desktop/aeid_100_fp_invitrodbv2_dp.tsv', sep='\t')
y = np.array(df['measured_value_dn'])
df = df.drop(['measured_value_dn','dsstox_compound_id'], 1)
X = np.array(df.as_matrix())

X_, X_test, y_, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# fix parameters for gridsearch
spw = len(y[y == 0]) / len(y[y == 1])
fix_params = { 'max_depth': 14, 'n_estimators': 1000, 'objective': 'binary:logistic', 'learning_rate':0.4, 'scale_pos_weight':spw}

# parameters for tuning in gridsearch
CV1 = {'min_child_weight':[0, 1, 2], 'subsample':[0, 0.5, 0.6, 1], 'colsample_bytree':[0.6, 0.7, 0.8, 0.9], 'max_delta_step': [0], 'gamma':[x/10.0 for x in range(0, 5)]}

# GRID SEARCH ROUND 1
GS1 = GridSearchCV(xgb.XGBClassifier(**fix_params), CV1, scoring ='roc_auc', cv=5, n_jobs=30)
GS1.fit(X_, y_)
params_final = GS1.best_params_
print(params_final)
final_model = xgb.XGBClassifier(**params_final)
final_model.fit(X_, y_, verbose=False)

# Performance train
train_y_pred = final_model.predict(X_)
auc = roc_auc_score(y_, train_y_pred)
print("Performance train : ", auc)

# Performance test
test_y_pred = final_model.predict(X_test)
auc = roc_auc_score(y_test, test_y_pred)
print("Performance test : ", auc)

#
from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(y_, final_model.predict(X_)).ravel()
# Error rate :
err_rate = (fp + fn) / (tp + tn + fn + fp)
print("Error rate  : ", err_rate)
# Accuracy :
acc_ = (tp + tn) / (tp + tn + fn + fp)
print("Accuracy  : ", acc_)
# Sensitivity :
sens_ = tp / (tp + fn)
print("Sensitivity  : ", sens_)
# Specificity
sp_ = tn / (tn + fp)
print("Specificity  : ", sens_)
# False positive rate (FPR)
FPR = fp / (tn + fp)
print("False positive rate  : ", FPR)

# Error rate :
err_rate = (fp + fn) / (tp + tn + fn + fp)
print("Error rate  on train set : ", err_rate)
# Accuracy :
acc_ = (tp + tn) / (tp + tn + fn + fp)
print("Accuracy  on train set  : ", acc_)

tn, fp, fn, tp = confusion_matrix(y_test, final_model.predict(X_test)).ravel()
# Error rate :
err_rate = (fp + fn) / (tp + tn + fn + fp)
print("Error rate  on test set : ", err_rate)
# Accuracy :
acc_ = (tp + tn) / (tp + tn + fn + fp)
print("Accuracy  on test set  : ", acc_)

