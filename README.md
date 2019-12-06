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

### How to set up the workers

- To run the name server use the command 'pyro4ns -n <hostname>
- In the worker code specify the same hostname and port you used above
- Run the worker(s) using Python <worker filename>
- In the main server you must pass Name Server's hostname and port as an arguement in the locateNS() function
  
### Libraries used in this project

- Pyro4 for communication between main server and workers
- Sklearn for generating random forest models
- PyMySQL for accessing our database from the main server
- Flask to build our main server
