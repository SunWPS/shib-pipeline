import os

from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError


credentials = "tweets_private_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials

timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = "projects/learn-de-331908/subscriptions/tweets-sub"


def callback(message):
    print(message)
    print(message.data)
    message.ack()


streaming_pull = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for messages on " + subscription_path)

with subscriber:
    try:
        streaming_pull.result() # add time out in the result(), if you want
    except TimeoutError:
        streaming_pull.cancel()
        streaming_pull.result()
