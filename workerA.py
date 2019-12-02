from __future__ import print_function
import time
import Pyro4
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# TODO: THIS IS ALWAYS THE IP OR URL OF THE MACHINE YOUR SERVER RUNS ON
HOST_IP = "192.168.0.32"    # Set to the server ip or url(if on AWS)
HOST_PORT = 9092         # Set accordingly (i.e. 9876)

# Pyro4.config.SERIALIZERS_ACCEPTED = []
Pyro4.config.SERIALIZERS_ACCEPTED = ["json", "marshal", "serpent", "pickle"]

@Pyro4.expose
class ForestWorker(object):
    
    def __init__(self):
        pass

    def hello(self):
        return "Hello from worker A"

    def forest(self):

        features = self.features
        print("Creating labels...")
        # labels are the thing we are trying to predict
        labels_1 = np.array(features['avg_temp_future'])
        labels_2 = np.array(features['max_temp_future'])
        labels_3 = np.array(features['min_temp_future'])
        labels = np.column_stack((labels_1,
                                  labels_2,
                                  labels_3))
        print("Gathering features...")
        features = features.drop(['avg_temp_future',
                                  'max_temp_future',
                                  'min_temp_future'],
                                 axis=1)


        feature_list = list(features.columns)
        features = np.array(features)
        print("Created train and test subsets...")
        train_features, test_features, train_labels, test_labels = train_test_split(features,
                                                                                    labels,
                                                                                    test_size=0.25,
                                                                                    random_state=42)
        print("Generating forest...")
        # our forest
        rf = RandomForestRegressor(n_estimators=1000, random_state=42)
        print("Fitting data...")
        rf.fit(train_features, train_labels)

        print("Gathering predictions")
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

        response = {'predictions': predictions, 'accuracy': accuracy}

    def setFeatures(self, features):
        print("Received data from central server.")
        self.features = pd.read_json(features, orient='records')


if __name__ == "__main__":
    # Add the proper "host" and "port" arguments for the construction
    # of the Daemon so it can be accessed remotely
    with Pyro4.Daemon(host=HOST_IP, port=HOST_PORT) as daemon:
        # register the class
        worker_uri = daemon.register(ForestWorker)
        with Pyro4.locateNS() as ns:
            ns.register("forest.worker.a", worker_uri)
        print("Forest worker A available.")
        daemon.requestLoop()
