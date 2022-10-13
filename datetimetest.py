import pandas as pd
from datetime import time

y = pd.Timestamp('2022-10-10T4:20')
z = y.strftime("%H:%M:%S")
converted = pd.to_datetime(z, "%H:%M:%S")
print(z)
#x = time(3, 35, 0)
#print(x)
night_start = time(0, 0, 0)
night_end = time(5, 59, 59)
is_night = z > night_start
print(is_night)
#is_night = (x.time > night_start) & (x.time < night_end)
#print(is_night)