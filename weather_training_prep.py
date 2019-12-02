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

features = pd.read_csv('KATL.csv')

# # labels are the thing we are trying to predict
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
                          labels_3,
                          labels_4,
                          labels_5,
                          labels_6,
                          labels_7,
                          labels_8,
                          labels_9))

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

# example day for Nov/25/2019 at ATL airport
d = {'': [0],
     'year': [2019],
     'month': [11],
     'day': [25],
     'min_temp': [37],
     'max_temp': [63],
     'avg_temp': [48.46],
     'min_humidity': [37],
     'max_humidity': [86],
     'avg_humidity': [64],
     'min_uv_vis': [10],
     'max_uv_vis': [10],
     'avg_uv_vis': [10],
     'min_pressure': [28.79],
     'max_pressure': [28.87],
     'avg_pressure': [28.82],
     'min_wind_spd': [0],
     'max_wind_spd': [8],
     'avg_wind_spd': [3.875],
     'mode_wind_dir': [270],
     'mode_sky_desc_Cloudy': [0],
     'mode_sky_desc_Drizzle Fog': [0],
     'mode_sky_desc_Fair': [1],
     'mode_sky_desc_Fair / Windy': [0],
     'mode_sky_desc_Fog': [0],
     'mode_sky_desc_Heavy Rain / Windy': [0],
     'mode_sky_desc_Light Drizzle': [0],
     'mode_sky_desc_Light Rain': [0],
     'mode_sky_desc_Light Snow': [0],
     'mode_sky_desc_Mostly Cloudy': [0],
     'mode_sky_desc_Mostly Cloudy / Windy': [0],
     'mode_sky_desc_Partly Cloudy': [0],
     'mode_sky_desc_Rain': [0],
     'mode_sky_desc_Smoke': [0],
     'mode_sky_desc_Wintry Mix': [0]
     }

test_data = pd.DataFrame(d).to_numpy()
predictions2 = rf.predict(test_data)
print('Getting next weeks prediction for Atlanta International Airport...')
print('AVG Temp: ' + str(predictions2[0][0]))
print('MAX Temp: ' + str(predictions2[0][1]))
print('MIN Temp: ' + str(predictions2[0][2]))
print('AVG Humidity: ' + str(predictions2[0][4]))
print('MAX Humidity: ' + str(predictions2[0][5]))
print('MIN Humidity: ' + str(predictions2[0][6]))
print('AVG Pressure: ' + str(predictions2[0][7]))
print('MAX Pressure: ' + str(predictions2[0][8]))
print('MIN Pressure: ' + str(predictions2[0][9]))



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
