import pandas as pd
import pytz
from datetime import datetime, time

dataset = pd.read_csv('..\data\log20140403.csv') #import the dataset for 2014-04-03
to_drop = ['zone', 'idx', 'norefer', 'noagent', 'browser'] #remove irrelevant columns
dataset.drop(to_drop, inplace=True, axis=1)
dataset.rename(columns={'extention':'doc'}, inplace=True) #rename column to be in line with the proper variable name as found on SEC.gov

dataset.insert(1, 'datetime', pd.to_datetime(dataset['date'] + dataset['time'], format = "%Y-%m-%d%H:%M:%S"), True) #convert date and time to one field with correct data type
#drop old date and time fields and reorder dataset
to_drop = ['date', 'time']
dataset.drop(to_drop, inplace=True, axis=1)

date_series = dataset.loc[:, 'datetime'] #create new series containing datetime values
date_series = date_series.dt.day_name() #find day of week for each datetime value in series
dataset = dataset.assign(dayofweek = date_series) #add the series to the dataset

#early morning
#night_start = time(0, 0, 0)
#night_end = time(5, 59, 59)
#is_night = (dataset['datetime'].dt.time > night_start) & (dataset['datetime'].dt.time < night_end)
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

dataset['extension'] = dataset['doc'].str.extract("(\.[0-9a-z]+$)") #extract file extensions from file names

print(dataset.tail())