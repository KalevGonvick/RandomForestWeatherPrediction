from __future__ import print_function
from flask import Flask
import pandas as pd
import time
import Pyro4
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# The two libraries below are just for the png creation of the tree
from sklearn.tree import export_graphviz
# import pydot

Pyro4.config.SERIALIZERS_ACCEPTED = ["json", "marshal", "serpent", "pickle"]

# print a nice greeting.
def say_hello():
    return '<p>Hello!</p>\n'


def get_weather():
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
            print("found worker: " + worker + " at " + uri)
            workers.append(Pyro4.Proxy(uri))
    if not workers:
        raise ValueError("No workers found. Make sure they are running.")

    print(workers)

    for worker in workers:
        response = worker.hello()
        print(response)
        # initialize the object with these values
        worker.setFeatures(train_features.tolist())
        worker.setLabels(train_labels.tolist())
        worker.setTestFeatures(test_features.tolist())
        worker.setTestLabels(test_labels.tolist())

        worker.forest()

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', say_hello)

application.add_url_rule('/getWeather', 'weather', get_weather)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.run(host='0.0.0.0')