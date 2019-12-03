from __future__ import print_function
import time
import Pyro4
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# TODO: THIS IS ALWAYS THE IP OR URL OF THE MACHINE YOUR SERVER RUNS ON
HOST_IP = "192.168.0.30"    # Set to the server ip or url(if on AWS)
HOST_PORT = 9093         # Set accordingly (i.e. 9876)

# Pyro4.config.SERIALIZERS_ACCEPTED = []
Pyro4.config.SERIALIZERS_ACCEPTED = ["json", "marshal", "serpent", "pickle"]


@Pyro4.expose
class ForestWorker(object):

    def __init__(self):
        pass

    def hello(self):
        print("reached the hello function of worker B")
        return "Hello from worker B"

    def forest(self, features_in, predictions_in):
        features = pd.read_json(features_in, orient='records')
        predictionData = pd.read_json(predictions_in, orient='records')
        print("Creating labels...")
        # labels are the thing we are trying to predict
        labels_1 = np.array(features['avg_temp_future'])
        labels_2 = np.array(features['max_temp_future'])
        labels_3 = np.array(features['min_temp_future'])
        labels_4 = np.array(features['avg_humidity_future'])
        labels_5 = np.array(features['max_humidity_future'])
        labels_6 = np.array(features['min_humidity_future'])
        labels_7 = np.array(features['avg_pressure_future'])
        labels_8 = np.array(features['max_pressure_future'])
        labels_9 = np.array(features['min_pressure_future'])
        labels = np.column_stack((labels_1,
                                  labels_2,
                                  labels_3,
                                  labels_4,
                                  labels_5,
                                  labels_6,
                                  labels_7,
                                  labels_8,
                                  labels_9))
        print("Gathering features...")
        features = features.drop(['avg_temp_future',
                                  'max_temp_future',
                                  'min_temp_future',
                                  'avg_humidity_future',
                                  'max_humidity_future',
                                  'min_humidity_future',
                                  'avg_pressure_future',
                                  'max_pressure_future',
                                  'min_pressure_future'],
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

        predictions_week = rf.predict(predictionData)

        response = {'predictions': {'Day 1': [predictions_week[0][0],
                                              predictions_week[0][1],
                                              predictions_week[0][2],
                                              predictions_week[0][3],
                                              predictions_week[0][4],
                                              predictions_week[0][5],
                                              predictions_week[0][6],
                                              predictions_week[0][7],
                                              predictions_week[0][8]],
                                    'Day 2': [predictions_week[1][0],
                                              predictions_week[1][1],
                                              predictions_week[1][2],
                                              predictions_week[1][3],
                                              predictions_week[1][4],
                                              predictions_week[1][5],
                                              predictions_week[1][6],
                                              predictions_week[1][7],
                                              predictions_week[1][8]],
                                    'Day 3': [predictions_week[2][0],
                                              predictions_week[2][1],
                                              predictions_week[2][2],
                                              predictions_week[2][3],
                                              predictions_week[2][4],
                                              predictions_week[2][5],
                                              predictions_week[2][6],
                                              predictions_week[2][7],
                                              predictions_week[2][8]],
                                    'Day 4': [predictions_week[3][0],
                                              predictions_week[3][1],
                                              predictions_week[3][2],
                                              predictions_week[3][3],
                                              predictions_week[3][4],
                                              predictions_week[3][5],
                                              predictions_week[3][6],
                                              predictions_week[3][7],
                                              predictions_week[3][8]],
                                    'Day 5': [predictions_week[4][0],
                                              predictions_week[4][1],
                                              predictions_week[4][2],
                                              predictions_week[4][3],
                                              predictions_week[4][4],
                                              predictions_week[4][5],
                                              predictions_week[4][6],
                                              predictions_week[4][7],
                                              predictions_week[4][8]],
                                    'Day 6': [predictions_week[5][0],
                                              predictions_week[5][1],
                                              predictions_week[5][2],
                                              predictions_week[5][3],
                                              predictions_week[5][4],
                                              predictions_week[5][5],
                                              predictions_week[5][6],
                                              predictions_week[5][7],
                                              predictions_week[5][8]],
                                    'Day 7': [predictions_week[6][0],
                                              predictions_week[6][1],
                                              predictions_week[6][2],
                                              predictions_week[6][3],
                                              predictions_week[6][4],
                                              predictions_week[6][5],
                                              predictions_week[6][6],
                                              predictions_week[6][7],
                                              predictions_week[6][8]]}, 'accuracy': accuracy}
        return response

if __name__ == "__main__":
    # Add the proper "host" and "port" arguments for the construction
    # of the Daemon so it can be accessed remotely
    with Pyro4.Daemon(host=HOST_IP, port=HOST_PORT) as daemon:
        # register the class
        worker_uri = daemon.register(ForestWorker)
        with Pyro4.locateNS() as ns:
            ns.register("forest.worker.b", worker_uri)
        print("Forest worker B available.")
        daemon.requestLoop()
