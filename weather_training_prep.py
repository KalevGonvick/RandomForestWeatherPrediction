import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# The two libraries below are just for the png creation of the tree
from sklearn.tree import export_graphviz
# import pydot

# !!!!This model needs work!!!!
# I need to modify the data to predict NEXT weeks weather
# To do this, I need to copy and shift +7 weather info to the row

features = pd.read_csv('KMIA.csv')

# # labels are the thing we are trying to predict
labels_1 = np.array(features['avg_temp_future'])
labels_2 = np.array(features['max_temp_future'])
labels_3 = np.array(features['min_temp_future'])
labels = np.column_stack((labels_1,
                          labels_2,
                          labels_3))

features = features.drop(['avg_temp_future',
                          'max_temp_future',
                          'min_temp_future'],
                         axis=1)


feature_list = list(features.columns)
features = np.array(features)
train_features, test_features, train_labels, test_labels = train_test_split(features,
                                                                            labels,
                                                                            test_size=0.25,
                                                                            random_state=42)
# our forest
rf = RandomForestRegressor(n_estimators=1000, random_state=42)
rf.fit(train_features, train_labels)

# Use the forest's predict method on the test data
predictions = rf.predict(test_features)

# Calculate the absolute errors
errors = abs(predictions - test_labels)

# Print out the mean absolute error (mae)
print("Mean Abs Error: " + str(round(np.mean(errors), 2)))

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_labels)

# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy: ' + str(round(accuracy, 2)) + '%.')

#
# ##
# # --THE CODE BELOW IS JUST TO CREATE A PNG OF ONE OF THE TREES!!--
# # - Pulls a tree from the forest.
# # - Creates a .dot file
# # - Pydot creates png from dot file
#
# # tree = rf.estimators_[5]
# #
# # # Export the image to a dot file
# # export_graphviz(tree,
# #                 out_file='tree.dot',
# #                 feature_names=feature_list,
# #                 rounded=True,
# #                 precision=1)
# #
# # # Use dot file to create a graph
# # (graph, ) = pydot.graph_from_dot_file('./tree.dot')
# # # Write graph to a png file
# # graph.write_png('tree.png')
