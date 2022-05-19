# -*- coding: utf-8 -*-
"""
rawTweetExtract
Created on Sun Nov 28 19:00:33 2021

@author: de0
"""

import tweepy
import json
import os
import time
from datetime import datetime

#Change to a local directory containing rawTweets.txt file
os.chdir(os.getcwd())

#TODO: Change the file name to the json/text file you saved with YOUR credentials
with open("apiCredentials.json", "r") as credsfile:
    creds = json.load(credsfile)

credsfile.close()

#TODO: Make sure the keys in your dictionary match these below.
TWITTER_CONSUMER_KEY = creds["apiKey"]
TWITTER_CONSUMER_SECRET = creds["keySecret"]
TWITTER_ACCESS_TOKEN = creds["accessToken"]
TWITTER_ACCESS_TOKEN_SECRET = creds["accessTokenSecret"]

# Iterate and print tweets to txt file
rawfile = open('rawTweets.txt', 'a', newline='',encoding="utf-8")
tweetCounter = 0
begin = datetime.now()
start = time.time()

# you can play around with range number. See comment below by .items() of why we are doing this
# 125 iterations gets you 250k tweets (about the max you can pull in 24 hours with the rate limit)
for i in range (500):
    time.sleep(1)
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    
    tweets = tweepy.Cursor(api.search_tweets
                  , q = '*'
                  , tweet_mode = 'extended'
                  , lang="en").items(2000) # tweepy can bring in about 2000 tweets before we hit a rate limit
                                            # this makes sure that if we have to wait our API will pick back up with
                                            # the most recent tweets
    
    for tweet in tweets:
        tweet._json['replicated_at'] = str(datetime.now())
        rawfile.write(str(tweet._json) + '\n')
        tweetCounter += 1
        print ('tweetID#'
               + str(tweet.id)
               + ' has been stored successfully.')
        print ('tweetTimeStamp: '
               + str(tweet.created_at))
        print ('systemTimeStamp: '
               + str(datetime.now()))
        print ('Number of tweets successfully replicated: ' 
               + str(tweetCounter))
        print ('\n')

rawfile.close()
end = time.time()
finish = datetime.now()

# print some stats about the job
print ('Job start: '
       + str(begin))

print ('Job end: '
       + str(finish))

print ('Total Time: '
       + str((end-start)/3600)
       + ' hours'
       + '\n')

print ('Number of tweets successfully stored: ' 
       + str(tweetCounter))
