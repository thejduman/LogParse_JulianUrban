import pandas as pd
from datetime import time

def ts():
    y = pd.Timestamp('2022-10-10T4:20')
    z = y.time()
    print(z)
    #x = time(3, 35, 0)
    #print(x)
    night_start = time(0, 0, 0)
    night_end = time(5, 59, 59)
    #is_night = z > night_start
    #print(is_night)
    is_night = (z > night_start) & (z < night_end)
    print(is_night)

def seriescase():
    timevals = ['2022-10-10 03:00:00', '2022-10-10 05:20:00',
       '2022-10-10 07:40:00', '2022-10-10 10:00:00',
       '2022-10-10 12:20:00', '2022-10-10 14:40:00',
       '2022-10-10 17:00:00', '2022-10-10 19:20:00',
       '2022-10-10 21:40:00', '2022-10-11 00:00:00']
    #seriestest = pd.date_range(start="2022-10-10 03:00", end="2022-10-11 00:00", periods=10)
    #print(seriestest)
    timeseries = pd.Series(timevals)
    datetimeseries = pd.to_datetime(timeseries, format = "%Y-%m-%d %H:%M:%S")
    print(datetimeseries)
    a = datetimeseries.dt.hour
    #hourseries = pd.Series(a)
    #print(hourseries)
    #night_start = time(0, 0, 0)
    #night_end = time(5, 59, 59)
    timeofday = []
    for x in a:
        if (x > 0) & (x < 6): #night = 00:00-06:00
            timeofday.append("Night")
        if (x > 6) & (x < 12): #morning = 06:00-12:00
            timeofday.append("Morning")
        if (x > 12) & (x < 18): #afternoon = 12:00-18:00
            timeofday.append("Afternoon")
        if (x > 18) & (x < 24): #night = 18:00-00:00 (24 doesn't exist)
            timeofday.append("Evening")
    print(timeofday)
    timeofday_series = pd.Series(timeofday)
    print(timeofday_series)

seriescase()
