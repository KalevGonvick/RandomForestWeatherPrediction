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

    return "ITS FUCKING COLD"

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', say_hello)

application.add_url_rule('/getWeather', 'weather', get_weather)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.run()