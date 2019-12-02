from __future__ import print_function

import pymysql as pymysql
from flask import Flask
from flask import request
import pandas as pd
import time
import Pyro4
import logger
import json
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
# The two libraries below are just for the png creation of the tree
from sklearn.tree import export_graphviz
# import pydot

#create connection to database holding scraped data
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='capstone2019',
                             port=3306,
                             db='wundergroundpredictions')



Pyro4.config.SERIALIZERS_ACCEPTED = ["json", "marshal", "serpent", "pickle"]

# print a nice greeting.
def say_hello():
    return '<p>Hello!</p>\n'

#return the weather to the user
def get_weather():
    #find the airport code sent by the user
    airport = request.args.get('airport')

    #get all rows from the database
    query = "SELECT * FROM `wundergroundpredictions`.`katl`;"

    #send the query to the connected databse
    result = pd.read_sql(query, connection)
    #conver the result into a pandas dataframe
    features = pd.DataFrame(result, columns=['id','year','month','day','min_temp','max_temp','avg_temp','min_humidity',
                                          'max_humidity','avg_humidity','min_uv_vis','max_uv_vis','avg_uv_vis',
                                          'min_pressure','max_pressure','avg_pressure','min_wind_spd','max_wind_spd',
                                          'avg_wind_spd','mode_wind_dir','avg_temp_future','max_temp_future',
                                          'min_temp_future','avg_humidity_future','max_humidity_future',
                                          'min_humidity_future','avg_pressure_future','max_pressure_future',
                                          'min_pressure_future','mode_sky_desc_Cloudy','mode_sky_desc_Drizzle and Fog',
                                          'mode_sky_desc_Fair','mode_sky_desc_Fair / Windy','mode_sky_desc_Fog',
                                          'mode_sky_desc_Heavy Rain / Windy','mode_sky_desc_Light Drizzle',
                                          'mode_sky_desc_Light Rain','mode_sky_desc_Light Snow',
                                          'mode_sky_desc_Mostly Cloudy','mode_sky_desc_Mostly Cloudy / Windy',
                                          'mode_sky_desc_Partly Cloudy','mode_sky_desc_Rain','mode_sky_desc_Smoke',
                                          'mode_sky_desc_Wintry Mix'])
    #print the result
    print(features)


    #each worker is blank, but has the code to train and predict
    #every time the client wants the weather, train model with data from database
    #each worker is sent the date (from client)

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