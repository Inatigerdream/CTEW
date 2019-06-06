"""
### PARAMETERS ###
# TUNE #
learning_rate - shrinks weight on each step - tune
n_estimators - tune with learning rate?

# CONTROL OVERFITTING #
max_depth - max number of nodes in a row - recommended (3-10) but why even set a max? should be 729 in the case of descriptors
gamma - tune - global cutoff for significant nodes
min_child_weight - a smaller value is chosen because it is highly imbalanced class problem, and leaf nodes can have smaller sized groups
reg_lambda - L2 regularization term on weights (alias for lambda)

# IMBALANCED #
scale_pos_weight - for imbalanced datasets (ex if 90 negative obs and 10 pos set to ~9)
max_delta_step - maximum delta step we allow each leaf output to be - tune

# NOISE #
subsample - use to make model robust to noise
colsample_bytree - use to make model robust to noise
colsample_bylevel - subsample ratio of columns for each split can be done with colsample_bytree & subsample

# OTHER #
booster - assign booster type (gbtree/gblinear)
nthread - multithreading
n_jobs - multiprocessing
silent - gives running messages
objective - defines loss function to be minimized
reg_alpha - can be used in situations with high dimensionality to make algorithm run faster (alias for alpha)
base_score - inital prediction score of all instances
seed - deprecated
random_state - random number seed - makes model reproducible
missing - assign value to missing data
"""

import glob
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
from hpsklearn import HyperoptEstimator, xgboost_classification
from hyperopt import hp
from hyperopt.pyll.base import scope
from hyperopt.pyll.stochastic import sample
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

# run xgboost for files in test_aeids
for f in glob.glob('/home/rlougee/Desktop/test_aeids/*'):
    # read input file
    df = pd.read_csv(f, sep='\t')
    # get file name for outputs
    name = f.split('/')[-1][:-4]
    print(name)
    #output print statements into file
    sys.stdout = open('/home/rlougee/Desktop/test_aeids/{}_output.txt'.format(name),'w')

    # declare variables
    y = np.array(df['measured_value_dn'])
    df = df.drop(['measured_value_dn','dsstox_compound_id'], 1)
    X = np.array(df.as_matrix())
    X = X[:,~np.all(np.isnan(X), axis=0)]


    # make test and train data
    X_, X_test, y_, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    print('##########################')

    # calculate base parameters
    spw = len(y[y==0])/len(y[y==1])
    max_delta_step = 0 # hp.quniform('max_delta_step', 0, 1, .1)
    min_child_weight = hp.quniform('min_child',50,60,.1)
    # subsample = hp.quniform('subsample',0,1,0.1)
    colsample_bytree = 1 #hp.quniform('colsample_bytree',0.1,1,.1)
    # max_delta_step = hp.quniform('max_delta_step',0,10,1)
    gamma = hp.quniform('gamma',0.5,1,.01)
    learning_rate = hp.quniform('learning_rate',.01,.2,.001)
    n_estimators = sample(scope.int(hp.quniform('n_estimators',3000,4000,100)))
    max_depth = 100
    n_jobs = 30

    model = HyperoptEstimator(classifier=xgboost_classification('my_clf', min_child_weight=min_child_weight, colsample_bytree=colsample_bytree, max_delta_step=max_delta_step, gamma=gamma, learning_rate=learning_rate, n_estimators=n_estimators, max_depth=max_depth, scale_pos_weight=spw, reg_alpha=0, reg_lambda=1, colsample_bylevel=1, subsample=1 ))

    model.fit(X_, y_)
    a = str(model.best_model()['learner']).replace('=','":').replace('XGBClassifier(', '{"').replace(', ', ', "').replace(',\n       ', ', "').replace(')', '}').replace("'", '"').replace(' "missing":nan,','').replace(' "nthread":None,','').replace(' "silent":True,','').replace('"base_score":0.5, ','')
    print(a)
    import json
    params_final = json.loads(a)

    # print('##########################')
    #
    # cv1_params = {'min_child_weight':[3, 4, 5], 'subsample':[0, 0.5, 0.6, 1], 'colsample_bytree':[.6, .7, .8, .9], 'max_delta_step': [0],  'gamma':[x/10.0 for x in range(0, 5)]} #params to be tried in the grid search
    # fix_params = { 'max_depth': 14, 'n_estimators': 100, 'objective': 'binary:logistic', 'learning_rate':0.4, 'scale_pos_weight':spw}
    # csv1 = GridSearchCV(xgb.XGBClassifier(**fix_params), cv1_params, scoring ='roc_auc', cv=5, n_jobs=30)
    # csv1.fit(X_, y_)
    # # csv.grid_scores_
    # # print(csv1.cv_results_)
    # print(csv1.best_params_)
    #
    # # Performance train
    # train_y_pred = csv1.predict(X_)
    # auc = roc_auc_score(y_, train_y_pred)
    # print("Performance train : ", auc)
    #
    # # Performance test
    # test_y_pred = csv1.predict(X_test)
    # auc = roc_auc_score(y_test, test_y_pred)
    # print("Performance test : ", auc)
    #
    # print('##########################')
    #
    # cv2_fix_params = csv1.best_params_
    # cv2_params = {'learning_rate':[i/1000.0 for i in range(10, 30, 2)], 'n_estimators':[i for i in range(500, 1100, 100)]}
    # csv2 = GridSearchCV(xgb.XGBClassifier(**cv2_fix_params), cv2_params, scoring ='roc_auc', cv=5, n_jobs=30)
    # csv2.fit(X_, y_)
    # # print(csv2.cv_results_)
    # print(csv2.best_params_)
    #
    # print('##########################')
    #
    # # fix best_params_
    #
    # params_final = {**csv1.best_params_, **csv2.best_params_}
    # print('PARAMS FINAL', params_final)
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


    # #
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
    print("Specificity  : ", sp_)
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

    # print(list(zip(X.columns[2:], final_model.feature_importances_)))
    xgb.plot_tree(final_model, rankdir='LR')
    plt.savefig("/home/rlougee/Desktop/test_aeids/{}_treeplot".format(name), dpi=1200)
    xgb.plot_importance(final_model, importance_type="weight") #importance type (weight, gain, cover)
    plt.tight_layout()
    plt.savefig("/home/rlougee/Desktop/test_aeids/{}_featureimportance".format(name), dpi=1200)

    import pickle
    pickle.dump(final_model, open("/home/rlougee/Desktop/test_aeids/{}_model".format(name),'wb'))
    #loaded_mdel = pickle.load(open(file_name, 'rb'))