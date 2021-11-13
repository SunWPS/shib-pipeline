import os
import json
import datetime as dt

import tweepy
from google.cloud import pubsub_v1

import twitter_config


credentials = "tweets_private_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials

publisher = pubsub_v1.PublisherClient()
topic_path = "projects/learn-de-331908/topics/tweets"


class Stream_tweet(tweepy.Stream):
    
    
    def dt_change(self, date_time):
        dt_og = dt.datetime.strptime(date_time, "%a %b %d %H:%M:%S %z %Y")
        hours_change = dt.timedelta(hours=7)
        thai_dt = dt_og + hours_change
        real_dt = thai_dt.strftime("%Y-%m-%d %H:%M:%S")
        return real_dt
    
    
    def get_tw_dict(self, tweet):
        if "extended_tweet" in tweet:
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet["text"]

        tw = {"id": tweet["id_str"],
              "created_at": self.dt_change(tweet["created_at"]),
              "text": text,
              "username": tweet["user"]["screen_name"],
              "followers": tweet["user"]["followers_count"]}
        
        data = json.dumps(tw)
        message = data.encode("utf-8")
        
        publish = publisher.publish(topic_path, message)
        print("Publishd message id " + publish.result())
    
    
    def on_data(self, data):
        tweet = json.loads(data)
        
        if tweet["retweeted"] == False and "RT" not in tweet["text"] and tweet['in_reply_to_status_id'] == None:
            self.get_tw_dict(tweet)
            
    
    
    def on_error(self, status):
        print(status)
    

if __name__ == "__main__":
    hash_tag_list =  ["SHIBARMY", "SHIB"]
    stream = Stream_tweet(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET,
                      twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
    stream.filter(track=hash_tag_list)
    