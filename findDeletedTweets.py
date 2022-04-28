# -*- coding: utf-8 -*-
"""
findDeletedTweets
Created on Sun Nov 28 19:00:33 2021

@author: de0
"""

import os
import json
import ast
import time
from twython import Twython, TwythonError, TwythonRateLimitError
from datetime import datetime

#TODO: Each user will have a different seed. These variables will change based on # of users
user_seed = 0
count_other_users = 3

#TODO: Change to a local directory you want to store the raw txt files
os.chdir(r'Insert\Path\Here')

#open up the rawfile and see how many lines (tweets) we have.
# rawfile = open('rawTweets.txt', 'r',encoding="utf-8")
# num_lines = sum(1 for line in rawfile)
# print ('# of tweets to review: ' + str(num_lines))
# rawfile.close() 

#TODO: Make sure the file name is the same as the file name you used from the rawExtract.py
rawfile = open('rawTweets.txt', 'r',encoding="utf-8")

# TODO: if your program ever fails/crashes, use this block to restart where you left off.
leaveoff = 0
for i in range (leaveoff + user_seed):
    rawfile.readline()

#TODO: Change the file name to the json/text file you saved with YOUR credentials
with open("apiCredentials.json", "r") as credsfile:
    creds = json.load(credsfile)
    
credsfile.close()

#TODO: Make sure the keys in your dictionary match these below.
TWITTER_CONSUMER_KEY = creds["apiKey"]
TWITTER_CONSUMER_SECRET = creds["keySecret"]
TWITTER_ACCESS_TOKEN = creds["accessToken"]
TWITTER_ACCESS_TOKEN_SECRET = creds["accessTokenSecret"]

# open Twython cursor
twitter = Twython(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, 
                  TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

#look up random IDs if you want
# tweet = twitter.show_status(id=1487458062000484358)
# print (tweet)

# deletefile is the file that we will write deleted tweets to
deletefile = open('deletedTweets.txt', 'a', newline='',encoding="utf-8")

# accumulator to know how many lines(tweets) we have gone through
liveCounter = 0

# accumulator to know how many tweets appear to be deleted
deadCounter = 0

# magic
begin = datetime.now()
start = time.time()
while True:
    # read in tweets line by line and store the tweet ID
    print ('number of tweets reviewed: ' + str(liveCounter))
    print ('number of tweets deleted: ' + str(deadCounter))
    print ('System TimeStamp: ' + str(datetime.now()))
    print ('\n')
    line = rawfile.readline()
    if not line:
        break
    dictObj = ast.literal_eval(line) # converts the string to a dictionary
    idQuery = dictObj['id']
    try:
        #check twitter API for tweet ID
        tweet = twitter.show_status(id=idQuery)
        liveCounter += 1
    except TwythonRateLimitError:
        # we reached rate limit. Find how long we can wait and make the program wait to avoid a stop error
        remainder = float(twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
        print ('Waiting on API refresh...')
        print ('Time to wait: ' + str(remainder))
        time.sleep(remainder + 10) # just to be safe in case the remainder is <0
    except TwythonError as e:
        # we found an error - store the tweet in a new txt file because it may have been deleted
        deadCounter += 1
        errorMessage = '{}'.format(e)
        print (errorMessage)
        print ('TweetID: ' + str(dictObj['id']))
        print ('Deleted Tweet Count: ' + str(deadCounter))
        print ('\n')
        dictObj['TwythonError'] = errorMessage # add the error message to the dictionary object - to allow for query later
        deletefile.write(str(dictObj) + '\n')
        liveCounter += 1
    for i in range (count_other_users):
        rawfile.readline()


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

print ('Total tweets reviewed: ' + str(liveCounter))
print ('Total tweets deleted: ' + str(deadCounter))
   
rawfile.close()
deletefile.close()