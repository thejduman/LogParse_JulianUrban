import pandas as pd
import pytz
from datetime import datetime, time

print("Loading CSV file...")
dataset = pd.read_csv('..\data\log20140403.csv') #import the dataset for 2014-04-03

print("Pefroming initial data cleaning...")
to_drop = ['zone', 'idx', 'norefer', 'noagent', 'browser'] #remove irrelevant columns
dataset.drop(to_drop, inplace=True, axis=1)
dataset.rename(columns={'extention':'doc'}, inplace=True) #rename column to be in line with the proper variable name as found on SEC.gov

print("Reformatting datetime values...")
dataset.insert(1, 'datetime', pd.to_datetime(dataset['date'] + dataset['time'], format = "%Y-%m-%d%H:%M:%S"), True) #convert date and time to one field with correct data type
#drop old date and time fields and reorder dataset
to_drop = ['date', 'time']
dataset.drop(to_drop, inplace=True, axis=1)

print("Adding days of week column...")
date_series = dataset.loc[:, 'datetime'] #create new series containing datetime values
date_series = date_series.dt.day_name() #find day of week for each datetime value in series
dataset = dataset.assign(dayofweek = date_series) #add the series to the dataset

print("Adding time of day column...")
hours = dataset['datetime'].dt.hour
timeofday = []
for x in hours:
    if (x > 0) & (x < 6): #night = 00:00-06:00
        timeofday.append("Night")
    elif (x > 6) & (x < 12): #morning = 06:00-12:00
        timeofday.append("Morning")
    elif (x > 12) & (x < 18): #afternoon = 12:00-18:00
        timeofday.append("Afternoon")
    elif (x > 18) & (x < 24): #night = 18:00-00:00 (24 doesn't exist)
        timeofday.append("Evening")
timeofday_series = pd.Series(timeofday)
dataset['timeofday'] = timeofday_series


#night
#night_start = time(0, 0, 0)
#night_end = time(5, 59, 59)
#is_night = (dataset['datetime'].dt.time() > night_start) & (dataset['datetime'].dt.time() < night_end)
#print(is_night.head())
#morning
#morning_start = time(6, 0, 0)
#morning_end = time(11, 59, 59)
#is_morning = (dataset['datetime'].dt.time > morning_start) & (dataset['datetime'].dt.time < morning_end)
#afternoon
#afternoon_start = time(12, 0, 0)
#afternoon_end = time(17, 59, 59)
#is_afternoon = (dataset['datetime'].dt.time > afternoon_start) & (dataset['datetime'].dt.time < afternoon_end)
#evening
#evening_start = time(18, 0, 0)
#evening_end = time(23, 59, 59)
#is_evening = (dataset['datetime'].dt.time > evening_start) & (dataset['datetime'].dt.time < evening_end)

#assign data to columns
#dataset['timeofday'] = ''
#dataset.loc[is_night, 'timeofday'] = 'Night'
#print(dataset['timeofday'])
#dataset.loc[is_morning, 'timeofday'] = 'Morning'
#dataset.loc[is_afternoon, 'timeofday'] = 'Afternoon'
#dataset.loc[is_evening, 'timeofday'] = 'Evening'

print("Adding file extension column...")
dataset['extension'] = dataset['doc'].str.extract("(\.[0-9a-z]+$)") #extract file extensions from file names

print("The dataset is ready.")
print(dataset.head())
print(dataset.tail())
