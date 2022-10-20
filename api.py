import requests
import json
import re

def jprint(obj):
    text = json.dumps(obj, sort_keys=True)
    return text
response = requests.get("http://ip-api.com/json/128.32.73.122?fields=regionName")
data = jprint(response.json())
#print(type(data))

new_data = re.search("\{\"\w+\"\:\s\"(\w+)\"\}", data).group(1)
print(new_data)