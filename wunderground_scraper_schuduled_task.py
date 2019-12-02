# coding: utf-8

# This function is ONLY for getting large data scrapes for model training
# Use 'wunderground_scraper_scheduled_task' if you only want the summary of the current date

from datetime import datetime, timedelta
import schedule
import requests
import time
import json
import pandas

# url and header for fake browser
lookup_URL = 'https://api.weather.com/v1/location/{}:9:US/observations/historical.json'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
headers = {'User-Agent': user_agent}

def scrape_station(cur_station):

    current_date_station = datetime.date(datetime.now())
    end_date_station = current_date_station
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
        df = pandas.DataFrame(json_data_load['observations'])

        # format filename
        out_file_name = '{}-{}-{}.json'.format(current_date_station.year,
                                               current_date_station.month,
                                               current_date_station.day)

        print("Getting next weeks data for numpy labels")
        print("Summarizing Data for: " + out_file_name)
        # basic stat calculations for each day
        d = {'year': [current_date_station.year],
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
             'mode_sky_desc': [df['wx_phrase'].mode()[0]],
             'avg_wind_spd': [df['wspd'].mean()],
             'min_wind_spd': [df['wspd'].min()],
             'max_wind_spd': [df['wspd'].max()],
             'mode_wind_dir': [df['wdir'].mode()[0]],
             'avg_temp_future': [],
             'max_temp_future': [],
             'min_temp_future': [],
             'avg_humidity_future': [],
             'max_humidity_future': [],
             'min_humidity_future': [],
             'avg_pressure_future': [],
             'max_pressure_future': [],
             'min_pressure_future': [],
             }

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
                        'min_temp_future',
                        'avg_humidity_future',
                        'max_humidity_future',
                        'min_humidity_future',
                        'avg_pressure_future',
                        'max_pressure_future',
                        'min_pressure_future'
                        ]

        # reindex the columns
        new_df = new_df.reindex(columns=column_names)
        li.append(new_df)

        # increment 1 day
        current_date_station += timedelta(days=1)

    # concat everything into one data frame
    frame = pandas.concat(li, axis=0, ignore_index=True)
    new_frame = pandas.DataFrame(frame)

    # sort by year, month, day
    sorted_frame = new_frame.sort_values(by=['year', 'month', 'day'])
    sorted_frame = pandas.get_dummies(sorted_frame)

    # Push to DB
    ##################### PUSH TO DB HERE #####################


# For the purpose of this project, we are only scraping from KATL.
# Scraping takes about (~15 mins / airport * ~15 mins / year)
schedule.every().day.at("22:00").do(scrape_station('KATL'))

while True:
    schedule.run_pending()
    time.sleep(5)

