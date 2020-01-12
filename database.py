import requests
import json

url = "https://192.168.1.6:3000/api/cars"

def getData():
    global url
    request_data = requests.get(url, verify=False)
    return request_data.json()

def updateData(car):
    global url
    payload = car
    headers = {'content-type': 'application/json'}
    r = requests.put(url, data=json.dumps(payload), headers=headers, verify=False)
    return r.status_code


print(getData())