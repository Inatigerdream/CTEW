import pickle

import matplotlib.pyplot as plt
import xgboost as xgb

list0 = [176, 197, 225, 763, 795] #good cytox results
list1 = [2405, 2409, 2407, 222, 1898, 1882, 1813, 2483, 2477, 1870, 2064, 18, 1841, 2042, 2211, 214] #top test set perf

for i in list1:
    loaded_obj = pickle.load(open('/home/rlougee/Desktop/xgb_results/{}/{}_model'.format(i,i), 'rb'))
    print(i)
    # print(len(loaded_obj.feature_importances_), loaded_obj.feature_importances_)
    plt.bar(range(len(loaded_obj.feature_importances_)), loaded_obj.feature_importances_)
    xgb.plot_importance(loaded_obj, importance_type="weight") #importance type (weight, gain, cover)
    xgb.plot_tree(loaded_obj, rankdir='LR')
    plt.tight_layout()
    plt.show()


    # print(loaded_obj.feature_importances_[0])
# print(loaded_obj.predict([[random.randint(0,1) for i in range(729)]]))
