import pandas as pd

dataset = pd.read_csv('..\data\log20140403.csv') #import the dataset for 2014-04-03
to_drop = ['zone', 'idx', 'norefer', 'noagent', 'browser'] #remove irrelevant columns
dataset.drop(to_drop, inplace=True, axis=1)

dataset['datetime'] = pd.to_datetime(dataset['date'] + dataset['time'], format = "%Y-%m-%d%H:%M:%S") #convert date and time to one field with correct data type
#drop old date and time fields and reorder dataset
to_drop = ['date', 'time']
dataset.drop(to_drop, inplace=True, axis=1)
dataset = dataset['ip', 'datetime', 'cik', 'accession', 'extention', 'code', 'size', 'find', 'crawler']

#date_series = dataset.loc[:, 'datetime']
#dataset.assign(DayOfWeek = date_series.dt.day_name)

print(dataset.head)