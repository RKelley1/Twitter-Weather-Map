import requests, json
import pprint
import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import HeatMap
import json
import csv
import datetime


# r = requests.get('http://localhost:8000/get-tweet', params={'fromDate': '2018-04-20 00:00:00', 'toDate': '')

now = datetime.datetime.now()
currentDate = now.strftime("%Y-%m-%d %H:%M")
print(now.strftime("%Y-%m-%d %H:%M"))
#testing date format for http requests

#print('http://localhost:8000/get-tweet?fromDate='+ currentDate + ':00')


# r = requests.get('http://localhost:8000/get-tweet', params={'fromDate': '2018-04-20 00:00:00', 'toDate': '')
####use import datetime to get the current date into a variable and use in request below
#this will allow for the most recent to date version of the heatmap to be generated and displayed when visted in the browser


r = requests.get('http://localhost:8000/get-tweet?fromDate=2018-04-30 00:00:00')
data = r.json()
pprint.pprint(data)



# for k,v in data.items():
#     tmp = [ {
#                 'created_at': tweet['created_at'],
#                 'place': tweet['place']
#             }
#             for tweet in v
#             ]
#
# #pprint.pprint(tmp)
#
# keyList = ['created_at','place']
# testArr = []
# for row in tmp:
#     row2 = []
#     for key in keyList:
#         rep = row[key].split(',', 1)[0]
#         row2.append(rep)
#     row2.append(1)
#     testArr.append(row2)
#
# #print(testArr)
#
# #pprint.pprint(tmp)
#
# headers = ['tweet_date','city','occur']
# cityFrame = pd.DataFrame(testArr, columns=headers)
#
# #Sum all the occurances of tweets from the same city
# sumCity = cityFrame.groupby(by='city',as_index=False).sum()
#
# sumCity = pd.DataFrame(sumCity)
#
# #To get single lat and lon point for all cities that tweeted
# usCities = pd.read_json('cities.json')
# usCities = usCities[['city','latitude','longitude']]
#
#
# #Insert Lat and Lons for tweeted cities
# finalCity = sumCity.merge(usCities, on = 'city')
# #print(finalCity)
#
# #For proof of concept layer heat map
# snowCity = sumCity.merge(usCities, on = 'city')
#
# #MAP Data
# maxVal = float(finalCity['occur'].max())
# maxValSnow = float(snowCity['occur'].max())
#
# hmap = folium.Map(location=[39.183608, -96.571669], zoom_start=4,)
# #lat and long of the US region
#
# rainGroup = folium.FeatureGroup(name='Tweets About Rain')
# snowGroup = folium.FeatureGroup(name='Tweets About Snow')
#
# for_mapData = list(zip(finalCity.latitude.values, finalCity.longitude.values, finalCity.occur.values))
#
# heat = HeatMap(    for_mapData,
#                 min_opacity=0.5,
#                 max_val=maxVal,
#                 radius=20, blur=15,
#                 max_zoom=1,
#                 gradient={.25: 'lime', .5: 'green', .9: 'yellow', 1: 'red'}
#                 )
#
#
# snow = HeatMap(    list(zip(snowCity.latitude.values, snowCity.longitude.values, snowCity.occur.values)),
#                 min_opacity=0.5,
#                 max_val=maxValSnow,
#                 radius=5, blur=5,
#                 max_zoom=1,
#                 gradient={.25: 'lime', .5: 'green', .9: 'yellow', 1: 'red'}
#                 )
#
# rainGroup.add_child(heat)
# snowGroup.add_child(snow)
# hmap.add_child(rainGroup)
# hmap.add_child(snowGroup)
#
# hmap.add_child(folium.LayerControl())
# #fp = open('tmp.html', 'wb')
#
#
#
# #### need to dump generated html heatmap to a variable or file or call this python script
#     # in api/resources/twitter.py where the html is actually hosted to the web
#
# hmap.save('heatmap.html')
