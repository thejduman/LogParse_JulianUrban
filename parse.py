import pandas as pd
import pytz
from datetime import datetime, time

dataset = pd.read_csv('..\data\log20140403.csv') #import the dataset for 2014-04-03
to_drop = ['zone', 'idx', 'norefer', 'noagent', 'browser'] #remove irrelevant columns
dataset.drop(to_drop, inplace=True, axis=1)

dataset['datetime'] = pd.to_datetime(dataset['date'] + dataset['time'], format = "%Y-%m-%d%H:%M:%S") #convert date and time to one field with correct data type
#drop old date and time fields and reorder dataset
to_drop = ['date', 'time']
dataset.drop(to_drop, inplace=True, axis=1)
dataset = dataset[['ip', 'datetime', 'cik', 'accession', 'extention', 'code', 'size', 'find', 'crawler']]

date_series = dataset.loc[:, 'datetime'] #create new series containing datetime values
date_series = date_series.dt.day_name() #find day of week for each datetime value in series
dataset = dataset.assign(dayofweek = date_series) #add the series to the dataset

#early morning
early_morning_start = pytz.utc.localize(time(0, 0, 0))
early_morning_end = pytz.utc.localize(time(0, 6, 0))
is_early_morning = (dataset['datetime'] > early_morning_start) & (dataset.index < early_morning_end)
#morning
morning_start = pytz.utc.localize(time(0, 6, 1))
morning_end = pytz.utc.localize(time(0, 12, 0))
is_morning = (dataset['datetime'] > morning_start) & (dataset.index < morning_end)
#afternoon
afternoon_start = pytz.utc.localize(time(0, 12, 1))
afternoon_end = pytz.utc.localize(time(0, 18, 0))
is_afternoon = (dataset['datetime'] > afternoon_start) & (dataset.index < afternoon_end)
#evening
evening_start = pytz.utc.localize(time(0, 18, 1))
evening_end = pytz.utc.localize(time(0, 23, 59))
is_evening = (dataset['datetime'] > evening_start) & (dataset.index < evening_end)

#assign data to columns
dataset['timeofday'] = ''
dataset.loc[is_early_morning, 'timeofday'] = 'Early Morning'
dataset.loc[is_morning, 'timeofday'] = 'Morning'
dataset.loc[is_afternoon, 'timeofday'] = 'Afternoon'
dataset.loc[is_evening, 'timeofday'] = 'Evening'

print(dataset)