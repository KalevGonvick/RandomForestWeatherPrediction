# coding: utf-8

from datetime import datetime, timedelta

import requests
import os
import json
import pandas

def getnextweeksdata(date, cur_station):
    # url and header for fake browser
    lookup_URL = 'https://api.weather.com/v1/location/{}:9:US/observations/historical.json'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    headers = {'User-Agent': user_agent}

    # Format the lookup_URL for the current station
    formatted_lookup_URL = lookup_URL.format(cur_station)
    start_total_date = str(date.year)

    if date.month < 10:
        start_total_date += '0'
        start_total_date += str(date.month)
    else:
        start_total_date += str(date.month)
    if date.day < 10:
        start_total_date += '0'
        start_total_date += str(date.day)
    else:
        start_total_date += str(date.day)

    # Add the parameters to the URL
    params = {'apiKey': '6532d6454b8aa370768e63d6ba5a832e',
              'units': 'e',
              'startDate': start_total_date}

    # request the json page
    json_data = requests.get(formatted_lookup_URL,
                             params=params,
                             headers=headers
                             ).content

    json_data_load = json.loads(json_data)
    df = pandas.DataFrame(json_data_load['observations'])
    return [df['temp'].mean(), df['temp'].min(), df['temp'].max()]


def scrape_station(cur_station):

    # start and end date for scrape
    current_date = datetime(year=2015, month=1, day=1)
    end_date = datetime(year=2015, month=2, day=1)

    # create dirs for the data
    os.mkdir(cur_station + '_csv')

    # url and header for fake browser
    lookup_URL = 'https://api.weather.com/v1/location/{}:9:US/observations/historical.json'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    headers = {'User-Agent': user_agent}

    li = []
    while current_date != end_date:

        print("Scraping Date: " + str(current_date))

        # Format the lookup_URL for the current station
        formatted_lookup_URL = lookup_URL.format(cur_station)
        start_total_date = str(current_date.year)

        if current_date.month < 10:
            start_total_date += '0'
            start_total_date += str(current_date.month)
        else:
            start_total_date += str(current_date.month)
        if current_date.day < 10:
            start_total_date += '0'
            start_total_date += str(current_date.day)
        else:
            start_total_date += str(current_date.day)

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
        df = pandas.DataFrame(json_data_load['observations'])

        # format filename
        out_file_name = '{}-{}-{}.json'.format(   current_date.year,
                                                  current_date.month,
                                                  current_date.day)




        print("Geting next weeks data for numpy labels")

        nextDate = current_date + timedelta(days=7)
        nextDate_val_array = getnextweeksdata(nextDate, cur_station)

        print("Summarizing Data for: " + out_file_name)
        # basic stat calculations for each day
        d = {'year': [current_date.year],
             'month': [current_date.month],
             'day': [current_date.day],
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
             'mode_sky_desc': [df['wx_phrase'].mode()[0]],
             'avg_wind_spd': [df['wspd'].mean()],
             'min_wind_spd': [df['wspd'].min()],
             'max_wind_spd': [df['wspd'].max()],
             'mode_wind_dir': [df['wdir'].mode()[0]],
             'avg_temp_future': [nextDate_val_array[0]],
             'max_temp_future': [nextDate_val_array[2]],
             'min_temp_future': [nextDate_val_array[1]]}

        # create new data frame and explicitly set our column names + order
        new_df = pandas.DataFrame(d)
        column_names = ['year',
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
                        'mode_sky_desc',
                        'avg_temp_future',
                        'max_temp_future',
                        'min_temp_future'
                        ]

        # reindex the columns
        new_df = new_df.reindex(columns=column_names)
        li.append(new_df)

        # increment 1 day
        current_date += timedelta(days=1)

    frame = pandas.concat(li, axis=0, ignore_index=True)
    new_frame = pandas.DataFrame(frame)
    li = []

    sorted_frame = new_frame.sort_values(by=['year', 'month', 'day'])
    sorted_frame = pandas.get_dummies(sorted_frame)
    sorted_frame.to_csv('./' + cur_station + '_csv/' + cur_station + '.csv')


# START CALL HERE
# Scrape the airport codes in the list
for station in ['KMIA']:
    print("Scraping station: " + station)
    scrape_station(station)
