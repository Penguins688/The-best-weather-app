import pandas as pd
import requests
import time
import math
import subprocess

file_path = 'cities.xlsx'
df = pd.read_excel(file_path)
phone_number = input("Enter target phone number: ")

duplicate_columns = df.columns[df.columns.duplicated()]
if len(duplicate_columns) > 0:
    print(f"Duplicate columns found: {duplicate_columns}")

df.columns = ['city', 'lat', 'lng']

def request(lat, lng):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": "temperature_2m,precipitation,windspeed_10m",
        "temperature_unit": "fahrenheit"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if "hourly" in data:
        for hour in data["hourly"]["time"]:
            index = data["hourly"]["time"].index(hour)
            temperature = data["hourly"]["temperature_2m"][index]
            precipitation_mm = data["hourly"]["precipitation"][index]
            precipitation_in = math.floor(precipitation_mm / 25.4)
            windspeed = data["hourly"]["windspeed_10m"][index]

            return f"temperature: {temperature}°F, precipitation: {precipitation_in:.2f}in, windspeed: {math.floor(windspeed * 0.621371)}mph"
    else:
        return "Could not retrieve weather data."


time.sleep(3)

while True:
    for index, row in df.iterrows():
        lat = row['lat']
        lng = row['lng']
        city = row['city']
        string = f"Weather in {city}: " + request(lat, lng)
        subprocess.run(["osascript", "executables/message.scpt", phone_number, string])
