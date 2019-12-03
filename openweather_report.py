# -*- coding: utf-8 -*-
from typing import Optional, Tuple
import time
import json
import os
import pwd
import math
import requests

# easy way to get a degree sign in the output
deg = u'\N{DEGREE SIGN}'

# TODO: These should probably eventually be in a config file:
ow_api_key = "YOUR_OPENWEATHERMAP_API_KEY"
# How to get an API key: https://openweathermap.org/guide#how

location_code = "YOUR_LOCATION_CODE"
# You can get your location code by navigating to https://openweathermap.org
# and searching for your city. The location code will be displayed in the
# resulting URL.
# Ex: City name: New York, US -> https://openweathermap.org/city/5128581
# the location code is 5128581

# Get the running user's username for a personalized greeting.
username = os.getlogin()


def day_index(forecast: dict, forecast_day: int) -> Tuple[int, int]:
    # return the starting and ending indices for the requested day in forecast['list']

    # Openweathermap's free forecast provides 40 forecasted conditions in 3h
    # intervals, starting at midnight UTC.  date is given in Unix epoch in
    # forecast['list'][index]['dt'], and in ISO (UTC) text string in
    # forecast['list'][index][sys]['dt_txt'] look for where the day changes
    # in 'dt_txt'? - no, that only works in UTC. use the time library?

    current_day = time.localtime()[2]
    target_day = current_day + forecast_day

    # find the first index of the desired day:
    start_index = math.nan
    for i in range(0, 40):
        list_date = time.localtime(forecast['list'][i]['dt'])[2]
        if list_date == target_day:
            start_index = i
            break

    if start_index == math.nan:
        raise ValueError("Date out of range.")

    # now find the last index 
    # in the case that we are asking for the last day in the forecast file,
    # we SHOULD get this far in the function so we know where the day starts.
    # Just have it end on the last index since we won't see the next day.

    # TODO: the final index probably shouldn't be hardcoded; this leaves the
    # program vulnerable to changes in OWM's API.
    
    end_index = 39
    for j in range(start_index, 40):
        list_date = time.localtime(forecast['list'][j]['dt'])[2]
        if list_date == target_day + 1:
            end_index = j
            break

    return (start_index, end_index)


def max_temp(forecast: dict, forecast_day: int) -> float:
    # day 0: today, day 1: tomorrow, etc
    start_index, end_index = day_index(forecast, forecast_day)

    high_temp = -10000

    for i in range(start_index, end_index):
        forecast_high = forecast['list'][i]['main']['temp_max']
        if forecast_high > high_temp:
            high_temp = forecast_high

    return high_temp


def min_temp(forecast: dict, forecast_day: int) -> float:
    start_index, end_index = day_index(forecast, forecast_day)

    low_temp = 10000

    for i in range(start_index, end_index):
        forecast_low = forecast['list'][i]['main']['temp_min']
        if forecast_low < low_temp:
            low_temp = forecast_low

    return low_temp


def wcondition(forecast: dict, forecast_day: int) -> Tuple[str, float]:
    # TODO: The question here is how to decide what constitutes the weather
    # conditions for the day.  Just select an arbitrary timestamp and use
    # that condition?  Try to figure out what sticks the longest?  Currently
    # just using whatever's closest to the middle of the (remaining) day.
    # probably what we REALLY want to know is whether it will rain, storm,
    # or snow, no matter what time.  use condition id code:
    # forecast['list'][i]['weather']['id']
    # https://openweathermap.org/weather-conditions - 2XX thunderstorms, 3XX
    # drizzle, 5XX rain, 6XX snow 
    # may want to warn about tornadoes: code 781 and return average wind
    # speed? actually, this should probably be a separate function.

    start_index, end_index = day_index(forecast, forecast_day)
    midday = round(float((end_index - start_index) / 2))

    weather_condition = forecast['list'][midday]['weather'][0]['description']
    wind_speed = forecast['list'][midday]['wind']['speed']
    return weather_condition, wind_speed


# MAIN

# Fetch the weather reports
# TODO: allow unit choice. This is currently very American-centric.
forecast_json = requests.get(
    f"http://api.openweathermap.org/data/2.5/forecast?APPID={ow_api_key}&id={location_code}&units=imperial"
    )
forecast = forecast_json.json()
weather_json = requests.get(
    f"http://api.openweathermap.org/data/2.5/weather?APPID={ow_api_key}&id={location_code}&units=imperial"
    )
weather = weather_json.json()

# Openweathermap's UV index reports don't use the same location codes as the other weather reports; can only be fetched
# by latitude and longitude. Using the lat&lon from the weather file.
lat = weather['coord']['lat']
lon = weather['coord']['lon']

uvindex_json = requests.get(
    f"http://api.openweathermap.org/data/2.5/uvi/forecast?APPID={ow_api_key}&lat={lat}&lon={lon}&cnt=4"
    )
uvindex = uvindex_json.json()

if time.localtime()[3] < 12:
    greeting = "Good morning"
elif time.localtime()[3] < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

print(f"{greeting} {username}.")
print(
    f"The current time is {time.strftime('%I:%M %p', time.localtime())} on {time.strftime('%a, %b %d %Y', time.localtime())}."
    )
print(f"It is currently {round(weather['main']['temp'])}{deg}F in {weather['name']}.")
print(f"Current conditions: {weather['weather'][0]['description']} with {weather['wind']['speed']} mph winds.")
print(
    f"Today's high will be {round(max_temp(forecast, 0))}{deg}F and the low will be {round(min_temp(forecast, 0))}{deg}F.")
print(f"Today's maximum UV index is {uvindex[0]['value']}.")
print(
    f"Tomorrow's high will be {round(max_temp(forecast, 1))}{deg}F and the low will be {round(min_temp(forecast, 1))}{deg}F.")
print(
    f"Tomorrow's conditions: {wcondition(forecast, 1)[0]} with {wcondition(forecast, 1)[1]} mph winds and a max UV index of {uvindex[1]['value']}.")
