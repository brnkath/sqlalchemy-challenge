# sqlalchemy-challenge

SQLAlchemy and Flask challenge to create an API to display temperature information from weather stations in Hawaii

Contributor: Brian Kath

Repository Structure - 

	- Main folder
		- .gitignore file
		- README.md file
	- Sub-folders
		- SurfsUp
			- Resources
				- hawaii.sqlite
				- hawaii_measurements.csv
				- hawaii_stations.csv
			- app.py
			- climate_starter.ipynb

Overview - 

For the first part of this project, I used Jupyter Notebook, SQLAlchemy, SQLite, Pandas and Matplotlib to collect and analyze two csv files containing temperature and precipitation data from weather stations in Hawaii. The data was gathered from 9 different weather stations from over 7 years. I narrowed the data to the last twelve months of measurements from the weather station with the most measurements collected. I then created a bar graph and histogram to show the differences in both precepitation and temperature across the twelve month period used.

For the second part of this project, I used Flask, SQLAlchemy and SQLite to create an API to deliver weather information from the same two csv files as the first part of the project. I created 5 different API endpoints, which are listed and explained below.

	- Precipitation: This returns a JSON representation of a dictionary created for the last twelve month period of precipitation using date as the key and precipitation as the value.
	- Stations: This returns a JSON list of all stations from the dataset.
	- Tobs: This returns a JSON list of temperatures for the last twelve months from the weather station with the most measurements.
	- Start: This is a dynamic API call which takes in a single date as an input and returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a range starting at the specified date and all dates more recent.
	- Start/End: This is a dynamic API call which takes in two dates as input(start date and end date) and returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for the specified date range.

