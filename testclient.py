from __future__ import print_function
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

features = pd.read_csv('KMIA.csv')

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
    print(features)
    worker.setFeatures(features.to_json())

    worker.forest()
