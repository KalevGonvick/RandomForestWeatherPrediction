from __future__ import print_function
import time
import Pyro4
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

HOST_IP = "192.168.0.32"    # Set to the server ip or url(if on AWS)
HOST_PORT = 9092         # Set accordingly (i.e. 9876)


@Pyro4.expose
class ForestWorker(object):
    def __init__(self, features, labels, test_features, test_labels):
        self.train_features = features
        self.train_labels = labels
        self.test_features = test_features
        self.test_labels = test_labels

    def forest(self):
        # our forest
        rf = RandomForestRegressor(n_estimators=1000, random_state=42)
        rf.fit(self.features, self.labels)

        # Use the forest's predict method on the test data
        predictions = rf.predict(self.testFeatures)

        # Calculate the absolute errors
        errors = abs(predictions - self.testLabels)

        # Print out the mean absolute error (mae)
        print("Mean Abs Error: " + str(round(np.mean(errors), 2)))

        # Calculate mean absolute percentage error (MAPE)
        mape = 100 * (errors / self.testLabels)

        # Calculate and display accuracy
        accuracy = 100 - np.mean(mape)
        print('Accuracy: ' + str(round(accuracy, 2)) + '%.')

        response = {'predictions': predictions, 'accuracy': accuracy}

        return response

    @property
    def features(self):
        return self.train_features

    @property
    def labels(self):
        return self.train_labels

    @property
    def testFeatures(self):
        return self.test_features

    @property
    def testLabels(self):
        return self.test_labels


if __name__ == "__main__":
    # Add the proper "host" and "port" arguments for the construction
    # of the Daemon so it can be accessed remotely
    with Pyro4.Daemon(host=HOST_IP, port=HOST_PORT) as daemon:
        # register the class
        worker_uri = daemon.register(ForestWorker)
        with Pyro4.locateNS() as ns:
            ns.register("forest.worker", worker_uri)
        print("Forest worker available.")
        daemon.requestLoop()
