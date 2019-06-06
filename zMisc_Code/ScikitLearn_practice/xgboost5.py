import numpy as np
from xgboostextension import XGBFeature, XGBRanker
import pandas as pd

# import dataset
dataset = pd.read_csv('/home/rlougee/Desktop/invitrodb_v2_enrichments/CTEW_aeid_100_invitrodbv2_20180918/CTEW_Results/CT-Enriched_FP_aeid_100_invitrodbv2_20180918.tsv', delimiter='\t')
dataset = dataset.iloc[:,1:].as_matrix()

X = dataset[:,1:]
y = dataset[:,0]

# many ojectives can be used except rank:pairwise
fea = XGBFeature(objective='reg:logistic', max_depth=5, n_estimators=50)
fitModel = fea.fit(X, y)
# return the index of leaf index for each tree
y_predict = fea.predict(X)

print("predict:"+str(y_predict))
print("type(y_predict):"+str(type(y_predict)))
print("fea.get_params():"+str(fea.get_params()))

##############################################################################

# CASE_NUM = 20
# GROUPS_NUM = 4
#
# if CASE_NUM % GROUPS_NUM != 0:
#     raise ValueError('Cases should be splittable into equal groups.')
#
# # Generate some sample data to illustrate ranking
# X_features = np.random.rand(CASE_NUM, 4)
# y = np.random.randint(5, size=CASE_NUM)
# X_groups = np.arange(0, GROUPS_NUM).repeat(CASE_NUM/GROUPS_NUM)
#
#
# # Append the group labels as a first axis to the features matrix
# # this is how the algorithm can distinguish between the different
# # groups
# X = np.concatenate([X_groups[:,None], X_features], axis=1)
#
#
# # objective = rank:pairwise(default).
# # Although rank:ndcg is also available,  rank:ndcg(listwise) is much worse than pairwise.
# # So ojective is always rank:pairwise whatever you write.
# ranker = XGBRanker(n_estimators=150, learning_rate=0.1, subsample=0.9)
#
#
# ranker.fit(X, y, eval_metric=['ndcg', 'map@5-'])
# y_predict = ranker.predict(X)
#
# print("predict:"+str(y_predict))
# print("type(y_predict):"+str(type(y_predict)))
#