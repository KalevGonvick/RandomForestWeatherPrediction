# RandomForestWeatherPrediction

### About
This project is an application where weather data can be used for weather prediction.

### Specifics

- Random Forest Regression algorithm is used for the AI
- Work distribution for model training is done with Pyro RMI
- Weather data is scraped from Weather Underground

### How to use

- MySQL DB is needed on port 3306 (Set up your own credentials)
- 2 machines as workers minimum (Change IP settings in code)
- 1 machine as main server (Change UP settings in code)
- 1 client machine (change request IP to main servers IP)
- All firewall rules must be changed on your own network!
