import redis
import sys
import json
sys.path.append("/Users/owattenmaker/Projects/twitter_weather_api")
from api.data import TweetsQuery, UsersQuery
from api.config import config

tweets_query = TweetsQuery(config.get_db())
users_query = UsersQuery(config.get_db())

def main():

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)

    p.subscribe(**{'sub1': handler})
    p.run_in_thread(sleep_time=0.1)

def handler(message):
    tweet = json.loads(message['data'].decode())

    user = users_query.save_user(**tweet['user'])
    tweets_query.save_tweet(user['id'], **tweet['tweet'])

if __name__ == '__main__':
    main()
