import hug
import pprint
from datetime import datetime

from api.resources import ResourceAbstract
from api.types import ResourceTypes
from api.types.time import time_format
from api.methods import get, post, get_html
from api.data import TweetsQuery, UsersQuery
from api.config import config
from sample_data.mapWrapper import generateHMap
from api.fileObj import cities

class TwitterResource(ResourceAbstract):
    def __init__(self, root_path=None):
        super().__init__(root_path)
        self.tweets_query = TweetsQuery(config.get_db())
        self.users_query = UsersQuery(config.get_db())

    def get_type(self):
        return ResourceTypes.TWITTER

    @get.urls('/get_last_date')
    def get_last_date(self, request, response):
        return {'date': self.tweets_query.get_last_date()}

    @post.urls('/save_tweets')
    def save_tweets(self, request, response, data):
        for tweet in data:
            user = self.users_query.save_user(**tweet['user'])
            self.tweets_query.save_tweet(user['id'], **tweet['tweet'])
        return 'okay'

    @get.urls('/test_save')
    def test_things(self, request, response):
        fake_tweets = [
            {
                "tweet": {
                    "tweet_date": "Sun Apr 15 20:45:12 +0000 2018",
                    "place": "Jeddah, Kingdom of Saudi Arabia",
                    "tweet_text": "\u201cGood writing is supposed to evoke sensation in the reader. Not the fact that it is raining but\u2026 https://t.co/5i8YmkXOuO"
                },
                "user": {
                    "user_date": "Mon Feb 15 08:00:19 +0000 2016",
                    "screen_name": "theGwiththeB",
                    "twitter_id": 4912368658
                }
            },
            {
                "tweet": {
                    "tweet_date": "Sun Apr 15 16:26:03 +0000 2018",
                    "place": "Elvas, Portugal",
                    "tweet_text": "Today finally we arrived to #elvas in #portugal\ud83c\uddf5\ud83c\uddf9 . One day early because is #raining since\u2026 https://t.co/NylXNJEiXo"
                },
                "user": {
                    "user_date": "Sun Sep 28 05:09:39 +0000 2014",
                    "screen_name": "Mreistwieder",
                    "twitter_id": 2788471113
                }
            }
        ]

        for tweet in fake_tweets:
            user = self.users_query.save_user(**tweet['user'])
            self.tweets_query.save_tweet(user['id'], **tweet['tweet'])


    @get_html.urls('/heatmap')
    def gen_heatmap(self, request, response,
                    from_date: hug.types.text=None,
                    to_date: hug.types.text=None):

        # from_ = datetime.strptime(from_date, time_format) if from_date else None
        # to_ = datetime.strptime(to_date, time_format) if to_date else None
        data = self.tweets_query.get_tweets(from_date=from_date , to_date=to_date)
        generateHMap(data, cities)
        # print(from_date)
        # print(to_date)

        print(from_date)
        print(to_date)
        print(' ')
        print(' ')
        print(' ')
        print(' ')

        fp = open('heatmap.html')       #uses parent directory when map gets regenerated 

        return ''.join(fp.readlines())

##################################################
    @get.urls('/get-tweet')
    def get_tweet(self, request, response, fromDate: hug.types.text):
        data = self.tweets_query.get_tweets(from_date=fromDate)
        return data
###################Testing####################

    @get.urls('/get_stuff')
    def get_stuff(self, request, response):
        return data
