import json
import requests
import urllib.request


LAT = '41.2133'
LON = '61.3151'

API_KEY = '5747d6060ff31e78224bbf4403267468'
url = f'https://api.openweathermap.org/data/2.5/weather?q=Pitnak&units=metric&appid={API_KEY}'

# response = requests.get(url)
# print(response.json())


    # Send request and open connection
with urllib.request.urlopen(url) as response:
    # Read the raw HTTP string and parse into JSON
    raw_data = response.read()
    data = json.loads(raw_data)
    
    # Extract specific data properties from the payload
    city_name = data.get("name")
    temp = str(data["main"]["temp"])
    condition = data["weather"][0]["description"]
    
    print(f"Current weather in {city_name}: {temp}°C with {condition}.")



















# data = '[]'
# print(data)
# print(type(data))

# json_data = json.loads(data)
# print(json_data)
# print(type(json_data))

# json_data['number'] = '12:43, 2025-09-12'
# json_data['music'] = '13:21, 2026-05-12'
# print(json_data)
# print(type(json_data))

# data = json.dumps(json_data)

# print(data)
# print(type(data))

# json_data = json.loads(data)
# print(json_data)
# print(type(json_data))

# json_data.extend(['pewdiepie', 'mrbeast','FEZOT'])
# print(json_data)
# print(type(json_data))

# data = json.dumps(json_data)
# print(data)
# print(type(data))
