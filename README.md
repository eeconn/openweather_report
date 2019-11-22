# openweather_report

This is a project I started to learn how to work with JSON files in Python3. I was interested in using [OpenWeatherMap](https://openweathermap.org)'s API as a replacement for the defunct Yahoo! Weather API used for fetching weather reports in the  [conky-google-now](https://github.com/mariusv/conky-google-now) .conkyrc configuration, so I started this project to get a handle on how to fetch the forecast information in the format I want.

Currently, this script outputs a text weather report to the console:

```
$ python ./openweather.py 
Hello eeconn.
The current time is 11:09 AM on Fri, Nov 22 2019.
It is currently 57°F in Durham County.
Current conditions: light rain with 8.05 mph winds.
Today's high will be 64°F and the low will be 50°F.
Today's maximum UV index is 2.72.
Tomorrow's high will be 54°F and the low will be 44°F.
Tomorrow's conditions: overcast clouds with 4.94 mph winds and a max UV index of 2.37.
```

## HOW TO USE THIS PROGRAM

This must be run in python3. Python 2.7 and earlier will throw several errors.

You will need a free API key from OpenWeatherMap. Instructions for getting a key can be found at <https://openweathermap.org/guide#how>. You will also need your location code, which can be found by searching for your city at <https://openweathermap.org/city>. The location code will be listed at the end of the URL. For example, the weather report URL for New York City is <https://openweathermap.org/city/5128581>. The location code is 5128581.

Once you have the API key and location code, add them to openweather.py in place of "YOUR_OPENWEATHERMAP_API_KEY" and "YOUR_LOCATION_CODE"

```python
ow_api_key = "YOUR_OPENWEATHERMAP_API_KEY"
# How to get an API key: https://openweathermap.org/guide#how

location_code = "YOUR_LOCATION_CODE"
# You can get your location code by navigating to https://openweathermap.org
# and searching for your city. The location code will be displayed in the
# resulting URL.
# Ex: City name: New York, US -> https://openweathermap.org/city/5128581
# the location code is 5128581
```
