import requests as rq
import pandas as pd
import time
import datetime
import subprocess

with open("data/API_key.txt", "r") as file:
    WEATHER_API_KEY = file.read().strip()

with open("data/cities.txt") as file:
    cities = [line.strip() for line in file]
url = f"http://api.openweathermap.org/data/2.5/weather"
params = {"q" : "",
          "appid" : WEATHER_API_KEY,
          "units" : "metric"}
records = []
for city in cities:
    #Sending our GET request
    params["q"] = city
    response = rq.get(url, params=params)
    if response.status_code == 200:
        #Transforming data to JSON
        data = response.json()
    
        weather_record = {
            'city': city,
            'country': data['sys']['country'],
            'lon': data['coord']['lon'],
            'lat': data['coord']['lat'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'sea_level': data['main'].get('sea_level', None),
            'grnd_level': data['main'].get('grnd_level', None),
            'visibility': data.get('visibility', None),
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'wind_gust': data['wind'].get('gust', None),
            'clouds': data['clouds']['all'],
            'weather_main': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description'],
            'weather_icon': data['weather'][0]['icon'],
            'timezone': data['timezone']
        }
        records.append(weather_record)
        time.sleep(1)
        
df = pd.DataFrame(records)
df.to_csv(f"data/dataset_{datetime.date.today().strftime('%Y-%m-%d')}.csv", index=False)

try:
    subprocess.run(["git", "add", "data/*.csv"], check=True)
    commit_msg = "Daily weather dataset is updated"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push"], check=True)
except Exception as e:
    print(e)
    
# ============================================================
# AUTOMATION SETUP (run once in terminal):
#
# macOS / Linux:
#   crontab -e
#   then add this line (runs daily at 11:00):
#   0 11 * * * cd /Desktop/Weather_analysis && /usr/bin/python3 daily_collection.py
#
# Windows (Task Scheduler):
#   Create task → Trigger: Daily, 11:00
#   Action: Start a program → python daily_collector.py
#   Working directory: /path/to/project
# ============================================================