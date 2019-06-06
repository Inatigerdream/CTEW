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

import json
import os
import pickle
import sys

import numpy as np
import pandas as pd
import xgboost as xgb
from hpsklearn import HyperoptEstimator, xgboost_classification
from hyperopt import hp
from hyperopt.pyll.base import scope
from hyperopt.pyll.stochastic import sample
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from Enrichment_MySQL.enrich_mysql0.duplicate_handler_0 import handle_duplicates
from Enrichment_MySQL.enrich_mysql0.fillfp_0 import fillfp
from database.database_schemas import Schemas
from database.dsstox.compounds import Compounds
from database.dsstox.generic_substance_compounds import GenericSubstanceCompounds
from database.dsstox.generic_substances import GenericSubstances
from database.invitrodb.mc4 import Mc4
from database.invitrodb.mc5 import Mc5
from database.invitrodb.sample import Sample
from database.session import SQLSession

# GET ALL ASSAYS FROM MC5
# QUERY MC5 data for hitcalls and chemical IDs

mysession = SQLSession(Schemas.information_schema).get_session()

query0 = mysession.query( Compounds.dsstox_compound_id, Mc5.hitc, Mc5.aeid,) \
    .join(GenericSubstanceCompounds, Compounds.id == GenericSubstanceCompounds.fk_compound_id) \
    .join(GenericSubstances, GenericSubstances.id == GenericSubstanceCompounds.fk_generic_substance_id) \
    .join(Sample, Sample.chid == GenericSubstances.id) \
    .join(Mc4, Mc4.spid == Sample.spid) \
    .join(Mc5, Mc5.m4id == Mc4.m4id)

mc5_table = pd.DataFrame(list(query0))
# print(mc5_table.shape)
# print( mc5_table[mc5_table['aeid']==1086] )
# sys.exit(1)

# run xgboost for files in test_aeids



def makeXGB(myaeid):
    try:
        # output print statements into file
        os.makedirs("/home/rlougee/Desktop/xgb_results/" + str(myaeid))
        sys.stdout = open('/home/rlougee/Desktop/xgb_results/{}/{}_output.txt'.format(myaeid, myaeid), 'w')

        # prep data
        df = mc5_table[mc5_table['aeid'] == myaeid]
        df = df[['dsstox_compound_id', 'hitc']]
        df = handle_duplicates(df, 3)
        print("duplicates passed")
        df = fillfp(df, 1445)
        print("fillfp passed")
        # get file name for outputs
        name = myaeid
        print(name)

        # print(df)
        # declare variables
        y = np.array(df['hitc'])
        print(y)
        df = df.drop(['hitc','dsstox_compound_id'], 1)
        X = np.array(df.values)
        print(X.shape) ######
        print(X)
        # X = X[:,~np.all(np.isnan(X), axis=0)]
        # print(X)


        # make test and train data
        X_, X_test, y_, y_test = train_test_split(X, y, test_size=0.2, stratify=y)


        print('##########################')

        # calculate base parameters
        spw = len(y[y == 0])/len(y[y == 1])
        max_delta_step = 0  # hp.quniform('max_delta_step', 0, 1, .1)
        min_child_weight = hp.quniform('min_child',50,60,.1)
        # subsample = hp.quniform('subsample',0,1,0.1)
        colsample_bytree = 1 #hp.quniform('colsample_bytree',0.1,1,.1)
        # max_delta_step = hp.quniform('max_delta_step',0,10,1)
        gamma = hp.quniform('gamma', 0.5, 1, .01)
        learning_rate = hp.quniform('learning_rate', .01, .2, .001)
        n_estimators = sample(scope.int(hp.quniform('n_estimators', 3000, 4000, 100)))
        max_depth = 100
        n_jobs = 30

        model = HyperoptEstimator(classifier=xgboost_classification('my_clf', min_child_weight=min_child_weight, colsample_bytree=colsample_bytree, max_delta_step=max_delta_step, gamma=gamma, learning_rate=learning_rate, n_estimators=n_estimators, max_depth=max_depth, scale_pos_weight=spw, reg_alpha=0, reg_lambda=1, colsample_bylevel=1, subsample=1 ))

        model.fit(X_, y_)
        a = str(model.best_model()['learner']).replace('=','":').replace('XGBClassifier(', '{"').replace(', ', ', "').replace(',\n       ', ', "').replace(')', '}').replace("'", '"').replace(' "missing":nan,','').replace(' "nthread":None,','').replace(' "silent":True,','').replace('"base_score":0.5, ','')
        print(a)

        params_final = json.loads(a)

        ###############################################
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


        # os.makedirs("/home/rlougee/Desktop/xgb_results/" + myaeid)
        # print(list(zip(X.columns[2:], final_model.feature_importances_)))
        #xgb.plot_tree(final_model, rankdir='LR')
        #plt.savefig("/home/rlougee/Desktop/xgb_results/{}/{}_treeplot".format(name, name), dpi=1200)
        #xgb.plot_importance(final_model, importance_type="weight") #importance type (weight, gain, cover)
        #plt.tight_layout()
        #plt.savefig("/home/rlougee/Desktop/xgb_results/{}/{}_featureimportance".format(name,name), dpi=1200)
        pickle.dump(final_model, open("/home/rlougee/Desktop/xgb_results/{}/{}_model".format(name, name),'wb'))
        #loaded_mdel = pickle.load(open(file_name, 'rb'))
    except:
        print('FAILURE: {}'.format(myaeid))


# set number of threads OPENBLAS
# probably need to use more than one (5?)
# os.system(" export OMP_NUM_THREADS=1 & export USE_SIMPLE_THREADED_LEVEL3=1")

# p = Pool(1)
# p.map(makeXGB, mc5_table['aeid'].unique())

for i in mc5_table['aeid'].unique()[1181:]:
    print(i)
    makeXGB(i)