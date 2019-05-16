import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

p = r.pubsub(ignore_subscribe_messages=True)

def handler(message):
    print(message['data'])

p.subscribe(**{'sub1': handler})
thread = p.run_in_thread(sleep_time=0.001)

# for message in p.listen():
#     print(message['data'])
