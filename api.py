from multiprocessing.sharedctypes import Value
import requests
import json
import re
import time

def jprint(obj): #original function to get a JSON dump from a response
    text = json.dumps(obj, sort_keys=True)
    return text

def batch(obj): #get a response from a JSON array of up to 100 IP addresses
    response = requests.post("http://ip-api.com/batch?fields=regionName", json = obj) #pass in the IPs
    data = response.json() #returns a list of dictionaries
    #print(type(data))
    regionList = []
    for x in data: #get a list of only the values
        regionList.append(x["regionName"])
    return regionList

def apiCall(series): #An attempt at looping through IP values to get responses. This method has bugs and should not be used. The batch function is more efficient at passing in multiple values and should be used instead.
    rl = 45
    locList = []
    for ip in series:
        if int(rl) > 0:
            response = requests.get("http://ip-api.com/json/" + ip + "?fields=regionName") #pass in IP value to API URL
            rl = response.headers.get('X-Rl')
            print('X-Rl = ' + rl)
            data = response.json() #get response
            text = json.dumps(data, sort_keys=True) #JSON dump
            #print(text)
            region = re.search("\{\"\w+\"\:\s\"(.+)\"\}", text).group(1) #extract only the region name from the JSON response
            locList.append(region)
        elif int(rl) == 0:
            print("Timeout: too many requests")
            print("X-Ttl = " + response.headers.get('X-Ttl'))
            time.sleep(int(response.headers.get('x-Ttl')))
            rl = 45
            print("X-Ttl = " + response.headers.get('X-Ttl'))
            apiCall(ip)
    return locList
    #print(response.headers.get('X-Rl'))
    #if int(response.headers.get('X-Rl')) > 0:
    #    data = response.json() #get response
    #    text = json.dumps(data, sort_keys=True) #JSON dump
    #    region = re.search("\{\"\w+\"\:\s\"(\w+)\"\}", text).group(1) #extract only the region name from the JSON response
    #    return region
    #elif int(response.headers.get('x-Rl')) == 0:
    #    print("Timeout: too many requests")
    #    time.sleep(int(response.headers.get('x-Ttl')))
    #    apiCall(ip)

def singleValue(ip): #function for passing in a single IP value to get the regionName
    response = requests.get("http://ip-api.com/json/" + ip + "?fields=regionName") #pass in IP value to API URL
    data = response.json() #get response
    print(data)
    text = json.dumps(data, sort_keys=True) #JSON dump
    print(text)
    region = re.search("\{\"\w+\"\:\s\"(.+)\"\}", text).group(1) #extract only the region name from the JSON response
    return region

#response = requests.get("http://ip-api.com/json/128.32.73.122?fields=regionName")
#testval = singleValue("128.84.158.247") #testing the function
#print(testval)

