from geopy.geocoders import Nominatim
import requests
import geocoder
from countryinfo import CountryInfo
import json
import ephem
from datetime import datetime
from calendar import timegm
from math import degrees
import json


def get_details():

    request_deatils = requests.get("https://api.wheretheiss.at/v1/satellites/25544").json()
    value_list = []
    for i, v in request_deatils.items():
        if i in ['name', 'id', 'units', 'units']:
            pass
        else:
            value_list.append(str(v)) 
    return value_list

def ip_info(user_ip:None):
    if user_ip == None: 
        my_ip = requests.get("https://ident.me/").content.decode("UTF-8") 
    else:
        my_ip = user_ip
    print(my_ip)
    ip = geocoder.ip(my_ip)
    print(ip)
    return [ip.country, ip.city, ip.latlng]

def calculate_passes(n):
    lat, lon = ip_info(None)[2] 
    alt = (json.loads(requests.get(f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}&interpolation=cubic").text))['results'][0]['elevation']

    data = (requests.get("https://celestrak.org/NORAD/elements/stations.txt").text).split("\n")[0:3]
    tle = []
    for d in data:
        tle.append(d.rstrip())
    
    iss = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))
    # Set location
    location = ephem.Observer()
    location.lat = str(lat)
    location.long = str(lon)
    location.elevation = alt

    # Override refration calculation
    location.pressure = 0
    location.horizon = '10:00'

    # Set time now
    now = datetime.utcnow()
    location.date = now

    # Predict passes
    passes = []
    for p in range(n):
        tr, azr, tt, altt, ts, azs = location.next_pass(iss)
        duration = int((ts - tr) * 60 * 60 * 24)
        year, month, day, hour, minute, second = tr.tuple()
        dt = datetime(year, month, day, hour, minute, int(second)).strftime("%Y-%m-%d %H:%M:%S")
        if duration > 60:
            passes.append({"risetime":dt, "duration": duration})
        location.date = tr + 25*ephem.minute

    # Return object
    obj = {
        "altitude": alt,
        "passes": n,
        "response": passes
    }
    
    return obj

def return_data(n:int):

    details = get_details()
    iss_obj = calculate_passes(n)
    imp_json_data = {
        
        "latitude": details[0],
        "longitude": details[1],
        "Altitude (km)": details[2],
        "Velocity (km/h)": details[3],
        'Station Time': datetime.utcfromtimestamp(int(details[6])).strftime("%Y-%m-%d %H:%M:%S"),
        "Is in Earth's shadow":True if details[4] == 'eclipsed' else False,
        "Footprint": details[5],
        "People in ISS": (requests.get("http://api.open-notify.org/astros.json").json())['people'],
        "Current ISS location": "https://maps.google.com/?q={0},{1}&ll={0},{1}&z=3".format(details[0], details[1]),
        "Current_local_time": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "iss data": iss_obj
    }
    return imp_json_data
