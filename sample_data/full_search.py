#!/usr/bin/python

import json
import redis
import requests

from datetime import datetime
from dateutil import parser
from searchtweets import *
from time import sleep

POLLING_RATE = 600 # 10 minutes in seconds
CHANNEL = 'sub1'
TWITTER_DATE_FORMAT = '%Y%m%d%H%M'
SERVER_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
BASE_URL = 'http://bigdickdata.us-west-2.elasticbeanstalk.com'
# BASE_URL = 'http://localhost:8000'


def main():
    now = datetime.now()
    to_date = now.strftime(TWITTER_DATE_FORMAT)

    server_date = requests.get(f'{BASE_URL}/get_last_date').json().get('data', {}).get('date', None)
    from_date = datetime.strftime(parser.parse(server_date or '2018-01-01T00:00:00+00:00'), TWITTER_DATE_FORMAT)

    enterprise_search_args = load_credentials('sample_data/creds.yaml', yaml_key='search_tweets_enterprise', env_overwrite=False)

    # gen_rule_payload is a function to format filter rules for API calls but will not accept the args we need to filter
    #rule = gen_rule_payload("is raining", "has:geo", from_date="2018-04-15", to_date="2018-04-16", results_per_call=100)

    #this is the rule filter we should start with to catch ppl talking about rain by location
    rule = {'query': '"is raining" lang:en place_country:us has:geo',
            'maxResults': 500,
            'toDate': to_date,
            'fromDate': from_date}
    tweets = collect_results(rule,
                             max_results=500,
                             result_stream_args=enterprise_search_args)

    data = [{
        'tweet': {
            'tweet_date': tweet['created_at'],
            'place': tweet['place']['full_name'],
            'tweet_text': tweet['text']
        },
        'user': {
            'user_date': tweet['user']['created_at'],
            'screen_name': tweet['user']['screen_name'],
            'twitter_id': tweet['user']['id']
        }
    } for tweet in tweets]

    r = redis.StrictRedis()

    for tweet in data:
        r.publish(CHANNEL, json.dumps(tweet))

    print(f'pushed {len(tweets)} new tweets')


if __name__ == '__main__':
    while 1:
        main()
        sleep(POLLING_RATE)
