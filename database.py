import requests
import json

url = "http://192.168.43.92:3000/api/cars/"

def getData(id=""):
    global url
    request_data = requests.get(url+str(id), verify=False)
    return request_data.json()

def updateData(carId, leftspeed, rightspeed, leftlinesensor, rightlinesensor, ultrasonicsensor):
    global url
    payload = {"id":carId, "leftspeed":leftspeed, "rightspeed":rightspeed, "leftlinesensor":leftlinesensor, "rightlinesensor":rightlinesensor, "ultrasonicsensor":ultrasonicsensor}
    headers = {'content-type': 'application/json'}
    r = requests.put(url, data=json.dumps(payload), headers=headers, verify=False)
    return r.status_code