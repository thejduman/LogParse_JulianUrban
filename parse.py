#dataset URL: http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/2014/Qtr2/log20140403.zip
import pandas as pd
import random
import matplotlib.pyplot as plt
import api
#from datetime import datetime, time

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
hours = dataset['datetime'].dt.hour #extract hours from datetime field
timeofday = []
for x in hours: #loop to select time of day
    if (x > 0) & (x < 6): #night = 00:00-06:00
        timeofday.append("Night")
    elif (x > 6) & (x < 12): #morning = 06:00-12:00
        timeofday.append("Morning")
    elif (x > 12) & (x < 18): #afternoon = 12:00-18:00
        timeofday.append("Afternoon")
    elif (x > 18) & (x < 24): #evening = 18:00-00:00 (24 doesn't exist)
        timeofday.append("Evening")
    #else: #causing all values to be "No Value", will re-add and debug if absolutely necessary
    #    timeofday.append("No Value")
timeofday_series = pd.Series(timeofday)
dataset['timeofday'] = timeofday_series

print("Adding file extension column...")
dataset['extension'] = dataset['doc'].str.extract("(\.[0-9a-z]+$)") #extract file extensions from file names

print("Randomizing last octet of IP addresses...") #Not truly random, will attempt to add true randomness if there is extra time
#pass the ip values to a list, iterate through the list and add a random number to the last octet using regex
#for x in dataset.iterrows():
n = str(random.randrange(2, 255)) #generate random numbers for last octet
#n = np.random.randint(2, 255, len(dataset.index))
#dataset['ip'] = dataset['ip'].str.replace("([a-z]{3})", str(n)) #this line but with a list of ips instead of the actual field
dataset['ip'].replace(regex="([a-z]{3})", value=n, inplace=True)

print("Adding column for translated HTTP log codes...")
codes = dataset['code'] #pass the code field into a list for easier parsing
http = []
for x in codes: #append values to the http list for each possible HTTP log code
    if x == 200:
        http.append("OK")
    elif x == 206:
        http.append("Partial Content")
    elif x == 301:
        http.append("Moved Permanently")
    elif x == 304:
        http.append("Not Modified")
    elif x == 400:
        x = http.append("Bad Request")
    elif x == 403:
        http.append("Forbidden")
    elif x == 404:
        http.append("Not Found")
    elif x == 500:
        http.append("Internal Server Error")
    elif x == 503:
        http.append("Service Unavailable")
    elif x == 504:
        http.append("Gateway Timeout")
http_series = pd.Series(http) #convert the list to a series
dataset['http'] = http_series #add the list to the dataset as a new column

print("Getting location data for IP addresses...")
ips = dataset['ip'].loc[0:99].to_list() #get a list of ip addresses
array = api.jprint(ips) #convert the ip list to json
ip_series = pd.Series(api.batch(ips)) #get an API response for the list of IP values and assign it to a new series
dataset['region'] = ip_series #add the series to the dataset as the region column

print("The dataset is ready.")
#print(dataset.head())
#print(dataset.tail())
#print(dataset['ip'])
#print(dataset['timeofday'].unique())

#Pie chart of which IPs accessed files most often across the day
x1 = dataset['ip'].value_counts()[:10]
pielabels = dataset['ip'].value_counts()[:10].index.to_list()
plt.pie(x1, labels=pielabels)
plt.title("IP Addresses with the Most Traffic to the Server")
plt.show()

#Bar chart of number of requests made during each time of day
x2 = dataset['timeofday'].value_counts(sort=False).index.to_list()
y2 = dataset['timeofday'].value_counts(sort=False)
plt.bar(x2, y2)
plt.title("Requests Made During Each Time of Day")
plt.xlabel("Time of day")
plt.ylabel("Number of requests made to server (in millions)")
plt.show()

#Bar chart of most frewuently accessed file types
x3 = dataset['extension'].value_counts()[:5].index.to_list()
y3 = dataset['extension'].value_counts()[:5]
plt.bar(x3, y3)
plt.title("File Types of the Most Frequently Accessed Files")
plt.xlabel("File type")
plt.ylabel("Number of requests for type of file (in millions)")
plt.show()