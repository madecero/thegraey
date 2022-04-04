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

#TODO: Change to a local directory you want to store the raw txt files
os.chdir(r'INSERT PATH')

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

#TODO: Make sure the file name is the same as the file name you used from the rawExtract.py
rawfile = open('rawTweets_0322.txt', 'r',encoding="utf-8")

# deletefile is the file that we will write deleted tweets to
deletefile = open('deletedTweets_raw_0322.txt', 'a', newline='',encoding="utf-8")

# open up the rawfile and see how many lines (tweets) we have.
num_lines = sum(1 for line in rawfile)
print ('# of tweets to review: ' + str(num_lines))
rawfile.close() 

# reopen the rawfile to scan for deleted tweets
rawfile = open('rawTweets_0322.txt', 'r',encoding="utf-8")

# accumulator to know how many lines(tweets) we have gone through
liveCounter = 0

# accumulator to know how many tweets appear to be deleted
deadCounter = 0

# if your program ever fails/crashes, use this block to restart where you left off.
leaveoff = 0
for i in range (leaveoff):
    rawfile.readline()

# magic
begin = datetime.now()
start = time.time()
for i in range (num_lines - leaveoff):
    # read in tweets line by line and store the tweet ID
    print ('number of tweets reviewed: ' + str(liveCounter))
    print ('number of tweets deleted: ' + str(deadCounter))
    print ('System TimeStamp: ' + str(datetime.now()))
    print ('\n')
    line = rawfile.readline()
    dictObj = ast.literal_eval(line) # converts the string to a dictionary
    idQuery = dictObj['id']
    try:
        #check twitter API for tweet ID
        tweet = twitter.show_status(id=idQuery)
        liveCounter += 1
        dictObj['TwythonError'] = 'N/A'
    except TwythonRateLimitError:
        # we reached rate limit. Find how long we can wait and make the program wait to avoid a stop error
        remainder = float(twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
        print ('Waiting on API refresh...')
        print ('Time to wait: ' + str(remainder))
        time.sleep(remainder + 10) # just to be safe in case the remainder is <0
        continue
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
