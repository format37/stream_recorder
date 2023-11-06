# import json
import datetime
import requests

url = 'https://stream.1tv.ru/api/schedule.json'
response = requests.get(url)
data = response.json()

current_time = datetime.datetime.fromtimestamp(data['channel']['current_time'])
schedule = data['channel']['schedule']['program']

current_shows = []
for item in schedule:
    start = datetime.datetime.fromtimestamp(item['begin']) 
    end = datetime.datetime.fromtimestamp(item['end'])
    if start <= current_time < end:
        current_shows.append(item['title'])

print('Current shows:', current_shows)
