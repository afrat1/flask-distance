import requests
from flask import Flask, request, jsonify,render_template
import json
import string
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

def distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c
    
    return distance

# Set the API endpoint URL
urlist = 'https://geocode-maps.yandex.ru/1.x/?apikey=6da42215-535b-4910-a5ca-28b7b380facb&format=json&geocode=Istanbul&result=1&lang=tr_TR'
url2 = 'https://geocode-maps.yandex.ru/1.x/?apikey=6da42215-535b-4910-a5ca-28b7b380facb&format=json&result=1&lang=tr_TR&geocode=fethiye'

flag = 1

try:
    response = requests.get(urlist)
    response_data = response.json()
    ist_list = response_data['response']['GeoObjectCollection']['featureMember']
    ip = ist_list[0]['GeoObject']['Point']['pos']
    print("Coordinates 1: " + ip)
    ip_istanbul = ip.split()
    x_istanbul= ip_istanbul[0]
    x_istanbul = float(x_istanbul)
    y_istanbul = ip_istanbul[1]
    y_istanbul = float(x_istanbul)
    #checking invalidity of coordinates
    if x_istanbul < -90 or x_istanbul > 90 or y_istanbul < -180 or y_istanbul > 180:
        print("Error: Invalid Istanbul coordinates")
        flag = 0;

except requests.exceptions.HTTPError as errh:
    print ("HTTP Error")
    flag = 0;
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting")
    flag = 0;
except requests.exceptions.Timeout as errt:
    print ("Timeout Error")
    flag = 0;
except requests.exceptions.RequestException as err:
    print ("Something Else")
    flag = 0;

try:
    response2 = requests.get(url2)
    response2.raise_for_status()
    response_data2 = response2.json()

    list2 = response_data2['response']['GeoObjectCollection']['featureMember']
    ip2 = list2[0]['GeoObject']['Point']['pos']
    print("Coordinates 2: " + ip)
    ip_2 = ip2.split()
    x_2= ip_2[0]
    x_2 = float(x_2)
    y_2 = ip_2[1]
    y_2 = float(y_2)
    if x_2 < -90 or x_2 > 90 or y_2 < -180 or y_2 > 180:
        print("Error: Invalid Fethiye Korfezi coordinates")
        flag = 0;

except requests.exceptions.HTTPError as errh:
    print ("HTTP Error")
    flag = 0;
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting")
    flag = 0;
except requests.exceptions.Timeout as errt:
    print ("Timeout Error")
    flag = 0;
except requests.exceptions.RequestException as err:
    print ("Something Else")
    flag = 0;


if(flag):
  distancee = distance(x_istanbul, y_istanbul, x_2, y_2)
  distancee = round(distancee,2)
  distancee = str(distancee)

@app.route("/", methods=["GET"])
def index():
    if(flag):
        return render_template('index.html', distancee=distancee)
        
    else:
        return render_template('oops.html')
        