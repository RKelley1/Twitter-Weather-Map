import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import HeatMap
import json
import csv


######TESTING CONVERSION OF TWEET DATA#####

testTweets = [
        {'created_at': '2018-04-30', 'place': 'West Palm Beach, FL'},
        {'created_at': '2018-04-31', 'place': 'San Diego, CA'},
        {'created_at': '2018-04-32', 'place': 'Los Angeles, CA'},
        ]

keyList = ['created_at','place']
testArr = []
for row in testTweets:
    row2 = []
    for key in keyList:
        rep = row[key].split(',', 1)[0]
        row2.append(rep)
    row2.append(1)
    testArr.append(row2)

print(testArr)

headers = ['tweet_date','city','occur']
cityFrame = pd.DataFrame(testArr, columns=headers)
print(cityFrame)


#Convert JSON data to CSV for data import to pandas dataframe
with open('visual_data.json', 'r') as handle:
    cityTweet = json.load(handle)

with open('tweet_data.csv', 'r') as inf:
    reader = csv.reader(inf.readlines())

with open('tweet_data.csv', 'w', newline='') as outf:
    writer = csv.writer(outf)
    writer.writerow(["tweet_date",'city','occur'])
    for cityTweet in cityTweet:
        writer.writerow([cityTweet["tweet"]["tweet_date"],
                         cityTweet["tweet"]["place"],'1'])




#Convert CSV in to List of Lists
cityArr = list(reader)
for row in cityArr[1:]:
    rep = row[1]
    rep = rep.split(',', 1)[0]
    row[1] = rep
    row[2] = int(row[2])




#Convert In to Pandas DataFrame
headers = cityArr.pop(0)
cityFrame = pd.DataFrame(cityArr, columns=headers)

#Sum all the occurances of tweets from the same city
sumCity = cityFrame.groupby(by='city',as_index=False).sum()

sumCity = pd.DataFrame(sumCity)

#To get single lat and lon point for all cities that tweeted
usCities = pd.read_json('cities.json')
usCities = usCities[['city','latitude','longitude']]

#Insert Lat and Lons for tweeted cities
finalCity = sumCity.merge(usCities, on = 'city')
print(finalCity)

#For proof of concept layer heat map
snowCity = sumCity.merge(usCities, on = 'city')

#MAP Data
maxVal = float(finalCity['occur'].max())
maxValSnow = float(snowCity['occur'].max())

hmap = folium.Map(location=[39.183608, -96.571669], zoom_start=4,)
#lat and long of the US region

rainGroup = folium.FeatureGroup(name='Tweets About Rain')
snowGroup = folium.FeatureGroup(name='Tweets About Snow')

for_mapData = list(zip(finalCity.latitude.values, finalCity.longitude.values, finalCity.occur.values))

heat = HeatMap(    for_mapData,
                   min_opacity=0.5,
                   max_val=maxVal,
                   radius=20, blur=15,
                   max_zoom=1,
                   gradient={.25: 'lime', .5: 'green', .9: 'yellow', 1: 'red'}
                 )


snow = HeatMap(    list(zip(snowCity.latitude.values, snowCity.longitude.values, snowCity.occur.values)),
                   min_opacity=0.5,
                   max_val=maxValSnow,
                   radius=5, blur=5,
                   max_zoom=1,
                   gradient={.25: 'lime', .5: 'green', .9: 'yellow', 1: 'red'}
                 )

rainGroup.add_child(heat)
snowGroup.add_child(snow)
hmap.add_child(rainGroup)
hmap.add_child(snowGroup)

hmap.add_child(folium.LayerControl())
#fp = open('tmp.html', 'wb')
hmap.save('heatmap.html')
