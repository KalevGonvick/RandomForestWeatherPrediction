from __future__ import print_function
import requests
import pymysql as pymysql
from flask import Flask
from flask import request
import pandas as pd
from datetime import datetime, timedelta
import time
import Pyro4
import json
import asyncio
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

def scrape_station(cur_station):

    # url and header for fake browser
    lookup_URL = 'https://api.weather.com/v1/location/{}:9:US/observations/historical.json'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    headers = {'User-Agent': user_agent}

    current_date_station = datetime.date(datetime.now()) - timedelta(days=7)
    end_date_station = current_date_station + timedelta(days=7)
    li = []
    while current_date_station != end_date_station:

        print("Scraping Date: " + str(current_date_station))

        # Format the lookup_URL for the current station
        formatted_lookup_URL = lookup_URL.format(cur_station)
        start_total_date = str(current_date_station.year)

        if current_date_station.month < 10:
            start_total_date += '0'
            start_total_date += str(current_date_station.month)
        else:
            start_total_date += str(current_date_station.month)
        if current_date_station.day < 10:
            start_total_date += '0'
            start_total_date += str(current_date_station.day)
        else:
            start_total_date += str(current_date_station.day)

        # Add the parameters to the URL
        params = {'apiKey':     '6532d6454b8aa370768e63d6ba5a832e',
                  'units':      'e',
                  'startDate':  start_total_date}

        # request the json page
        json_data = requests.get(formatted_lookup_URL,
                                 params=params,
                                 headers=headers
                                 ).content

        json_data_load = json.loads(json_data)
        df = pd.DataFrame(json_data_load['observations'])

        # format filename
        out_file_name = '{}-{}-{}.json'.format(current_date_station.year,
                                               current_date_station.month,
                                               current_date_station.day)

        print("Getting next weeks data for numpy labels")
        print("Summarizing Data for: " + out_file_name)
        # basic stat calculations for each day
        d = {'id': 0,
             'year': [current_date_station.year],
             'month': [current_date_station.month],
             'day': [current_date_station.day],
             'avg_temp': [df['temp'].mean()],
             'max_temp': [df['temp'].max()],
             'min_temp': [df['temp'].min()],
             'avg_humidity': [df['rh'].mean()],
             'max_humidity': [df['rh'].max()],
             'min_humidity': [df['rh'].min()],
             'avg_uv_vis': [df['vis'].mean()],
             'max_uv_vis': [df['vis'].max()],
             'min_uv_vis': [df['vis'].min()],
             'avg_pressure': [df['pressure'].mean()],
             'max_pressure': [df['pressure'].max()],
             'min_pressure': [df['pressure'].min()],
             'avg_wind_spd': [df['wspd'].mean()],
             'min_wind_spd': [df['wspd'].min()],
             'max_wind_spd': [df['wspd'].max()],
             'mode_wind_dir': [df['wdir'].mode()[0]],
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

        # create new data frame and explicitly set our column names + order
        new_df = pd.DataFrame(d)
        column_names = ['id',
                        'year',
                        'month',
                        'day',
                        'min_temp',
                        'max_temp',
                        'avg_temp',
                        'min_humidity',
                        'max_humidity',
                        'avg_humidity',
                        'min_uv_vis',
                        'max_uv_vis',
                        'avg_uv_vis',
                        'min_pressure',
                        'max_pressure',
                        'avg_pressure',
                        'min_wind_spd',
                        'max_wind_spd',
                        'avg_wind_spd',
                        'mode_wind_dir',
                        'mode_sky_desc_Cloudy',
                        'mode_sky_desc_Drizzle Fog',
                        'mode_sky_desc_Fair',
                        'mode_sky_desc_Fair / Windy',
                        'mode_sky_desc_Fog',
                        'mode_sky_desc_Heavy Rain / Windy',
                        'mode_sky_desc_Light Drizzle',
                        'mode_sky_desc_Light Rain',
                        'mode_sky_desc_Light Snow',
                        'mode_sky_desc_Mostly Cloudy',
                        'mode_sky_desc_Mostly Cloudy / Windy',
                        'mode_sky_desc_Partly Cloudy',
                        'mode_sky_desc_Rain',
                        'mode_sky_desc_Smoke',
                        'mode_sky_desc_Wintry Mix']

        # reindex the columns
        new_df = new_df.reindex(columns=column_names)
        li.append(new_df)

        # increment 1 day
        current_date_station += timedelta(days=1)

    # concat everything into one data frame
    frame = pd.concat(li, axis=0, ignore_index=True)
    new_frame = pd.DataFrame(frame)

    # sort by year, month, day
    sorted_frame = new_frame.sort_values(by=['year', 'month', 'day'])
    sorted_frame = pd.get_dummies(sorted_frame)

    return sorted_frame

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
    
    prediction_values = scrape_station('KATL')


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
        worker.setPredictionData(prediction_values.to_json())

        response = worker.forest()
        print(response)
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