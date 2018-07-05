
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json


# In[2]:


response = requests.get('https://api.darksky.net/forecast/**********/40.808071,-73.966412')
data = response.json()


# # "Right now it is TEMPERATURE degrees out and SUMMARY. Today will be TEMP_FEELING with a high of HIGH_TEMP and a low of LOW_TEMP. RAIN_WARNING."
# *TEMPERATURE is the current temperature<br>
# *SUMMARY is what it currently looks like (partly cloudy, etc - it's "summary" in the dictionary). Lowercase, please. <br>
# TEMP_FEELING is whether it will be hot, warm, cold, or moderate. You will probably use HIGH_TEMP and your own thoughts and feelings to determine this.<br>
# HIGH_TEMP is the high temperature for the day.<br>
# LOW_TEMP is the low temperature for the day.<br>
# RAIN_WARNING is something like "bring your umbrella!" if it is going to rain at some point during the day.<br>

# In[7]:


#navigate to current weather
current_weather = data['currently']
daily_weather = data['daily']['data'][0]


#start defining variables
temperature = current_weather['temperature']
summary = current_weather['summary']
temp_feeling = ''
high_temp = daily_weather['temperatureHigh']
low_temp = daily_weather['temperatureLow']
rain_chance = int(daily_weather['precipProbability'])
rain_warning = ''

#If for rain_warning
if rain_chance > 0.3:
    rain_warning = '. It might rain'
if rain_chance > 0.5:
    rain_warning = '. It will probably rain'
if rain_chance > 0.7:
    rain_warning ='. It will rain'

#If's for temp_feeling
if high_temp > 90:
    temp_feeling = 'hot as heck'
if high_temp > 80:
    temp_feeling = 'hot'
if high_temp < 79:
    temp_feeling = 'reasonable'
if high_temp < 69:
    temp_feeling = 'chilly'
if high_temp < 60:
    temp_feeling = 'cold'

today_forecast = "Right now it is {} degrees out and {}. Today will be {} with a high of {} and a low of {}{}.".format(temperature, summary, temp_feeling, high_temp, low_temp, rain_warning)
# print(today_forecast)


# In[8]:


right_now = datetime.datetime.now()
date_string = right_now.strftime("%B %d, %Y")

email_subject = "8AM Weather forecast " + date_string


# In[9]:


requests.post(
    "https://api.mailgun.net/v3/**********/messages",
    auth=("api", "*************"),
    data={"from": "M Albasi <**>",
          "to": ["M Albasi <**>"],
          "subject": email_subject,
          "text": today_forecast}) 

