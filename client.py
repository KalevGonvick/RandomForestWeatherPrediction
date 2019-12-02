from __future__ import print_function
import pandas as pd
import time
import Pyro4
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

workers = []

with Pyro4.locateNS() as ns:
    for worker, uri in ns.list(prefix="forest.worker").items():
        print("found market", worker)
        print("uri: ", uri)
        workers.append(uri)
if not workers:
    raise ValueError("no workers found! (have you started the workers?)")

print(workers)

Worker = Pyro4.Proxy(workers[0])   # get the remote object

Worker.hello()

# initialize the object with these values
Worker.setFeatures(features)
Worker.setLabels(labels)
Worker.setTestFeatures(test_features)
Worker.setTestLabels(test_labels)

# Worker.forest()

# worker = ForestWorker(features, labels, test_features, test_labels)


