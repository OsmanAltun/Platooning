import requests
import json


def getData():
    ship_api_url = "URL"
    request_data = requests.get(ship_api_url)
    return request_data.json()

def postData(car):
    url = 'URL'
    payload = car
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return r.status_code