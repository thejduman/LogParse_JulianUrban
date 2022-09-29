import pandas as pd

dataset = pd.read_csv('..\data\log20140403.csv') #import the dataset for 2014-04-03
to_drop = ['zone', 'idx', 'norefer', 'noagent', 'browser'] #remove irrelevant columns
dataset.drop(to_drop, inplace=True, axis=1)

date_series = pd.date_range(dataset.loc[:, 'date']).to_series
dataset.assign(DayOfWeek = date_series.dt.dayofweek)

print(dataset.head())