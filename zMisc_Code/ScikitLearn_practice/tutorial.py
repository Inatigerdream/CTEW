import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

# # # DECISION TREE # # #
#create tree object
# algorithms are gini or entropy
model = tree.DecisionTreeClassifier(criterion='entropy') # entropy tends to produce more balanced trees

# load iris flower data
from sklearn.datasets import load_iris

iris = load_iris()

x = iris.data[:,:2] # petal length and width
y = iris.target

print("### IRIS DATA ###")
print(iris.data)
print("\n### IRIS TARGET ###")
print(iris.target)


# x(predictor) y(target) x_test(predictor) of test_dataset
model.fit(x, y)
model.score(x, y)

#predict output
x_test = [[5,1.5]] # test 5cm long petals & 1.5cm wide iris flower
predicted = model.predict(x_test)

print("\n### TEST IRIS FLOWER ###\n", x_test)
print("\n### PREDICTED IRIS FLOWER ###\n", predicted)

# visualize decision tree
# to convert dot file to png on terminal:$ dot tree.dot -Tpng -o tree.png
from sklearn.tree import export_graphviz

export_graphviz(
    model,
    out_file="/home/rlougee/Desktop/iris_tree.dot",
    feature_names=iris.feature_names[2:],
    class_names=iris.target_names,
    rounded=True,
    filled=True
)



# # # # RANDOM FOREST # # #
#
# # x(predictor) y(target) x_test(predictor) of test_dataset
#
# # create random forest object
# model2 = RandomForestClassifier(n_estimators=1000)
#
# # Train the model using the training sets and check score
#
# model2.fit(x, y)
#
# # Predict Output
# predicted2 = model2.predict(x_test)
#
# # # # BOOSTING W/ XGBOOST # # #
# import xgboost as xgb
# # can boost with GBM but it has disadvantages
# # learning_rate determines how much each tree estimate impacts the model
#
# # n_estimators the number of sequential trees to be modeled
#
# # subsample the fraction of observations to be selected for each tree done by random sampling

