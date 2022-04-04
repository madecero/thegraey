# -*- coding: utf-8 -*-
"""
RawTweetsdb
Created on Fri Jan 28 20:30:41 2022

@author: de0
"""

import os
import ast
import sqlite3

#TODO: Change to a local directory you want to store the raw txt files
os.chdir(r'C:\Users\madec\Documents\de0project')

conn = sqlite3.connect('de0project.db') # open the connection
cursor = conn.cursor()

rawfile = open('rawTweetsFeb2022.txt', 'r', encoding="utf-8")
num_lines = sum(1 for line in rawfile)
print ('number of tweets to review: ' + str(num_lines))
print ('\n')
rawfile.close()

rawfile = open('rawTweetsFeb2022.txt', 'r', encoding="utf-8")
counter = 0

for i in range(num_lines):
    line = rawfile.readline()
    try:
        tweet = ast.literal_eval(line) # converts the string to a dictionary
    except ValueError:
        pass
    userList = []
    tweetList = []
    hashtagList = []
    mediaList = []
    urlList = []
    userList.append(tweet['user']['id'])
    userList.append(tweet['user']['name'])
    userList.append(tweet['user']['screen_name'])
    userList.append(tweet['user']['created_at'])
    userList.append(tweet['user']['description'])
    userList.append(tweet['user']['followers_count'])
    userList.append(tweet['user']['location'])
    userList.append(tweet['user']['verified'])
    tweetList.append(tweet['created_at'])
    tweetList.append(tweet['id'])
    tweetList.append(tweet['full_text'])
    tweetList.append(tweet['in_reply_to_user_id'])
    tweetList.append(tweet['in_reply_to_screen_name'])
    tweetList.append(tweet['in_reply_to_status_id'])
    try:
        tweetList.append(tweet['possibly_sensitive'])
    except KeyError:
        tweetList.append(False)
    tweetList.append(tweet['user']['id'])
    
    cursor.execute("INSERT OR IGNORE INTO UserData VALUES (?, ?, ?, ?, ?, ?, ?, ?);", userList)
    cursor.execute("INSERT OR IGNORE INTO TweetData VALUES (?, ?, ?, ?, ?, ?, ?, ?);", tweetList)
    
    if len(tweet['entities']['hashtags']) == 0:
        hashtagList.append(tweet['id'])
        hashtagList.append(None)
        cursor.execute("INSERT OR IGNORE INTO HashtagData VALUES (?, ?);", hashtagList)      
    else:
        for i in tweet['entities']['hashtags']:
            hashtagList = []
            hashtagList.append(tweet['id'])
            hashtagList.append(i['text'])
            cursor.execute("INSERT OR IGNORE INTO HashtagData VALUES (?, ?);", hashtagList)
    try:
        for i in tweet['entities']['media']:
            mediaList = []
            mediaList.append(tweet['id'])
            mediaList.append(i['media_url'])
            cursor.execute("INSERT OR IGNORE INTO MediaData VALUES (?, ?);", mediaList)
    except KeyError:
        mediaList.append(tweet['id'])
        mediaList.append(None)
        cursor.execute("INSERT OR IGNORE INTO MediaData VALUES (?, ?);", mediaList)
    if len(tweet['entities']['urls']) == 0:
        urlList.append(tweet['id'])
        urlList.append(None)
        cursor.execute("INSERT OR IGNORE INTO URlData VALUES (?, ?);", urlList)
    else:
        for i in tweet['entities']['urls']:
            urlList = []
            urlList.append(tweet['id'])
            urlList.append(i['expanded_url'])
            cursor.execute("INSERT OR IGNORE INTO URlData VALUES (?, ?);", urlList)
    
    counter += 1
    
    print ('number of tweets replicated: ' + str(counter))
    print ('\n')

rawfile.close()

#count* query if you are interested...
# query = '''
# SELECT COUNT(*) 
# FROM deletedData;
# '''

# viewResult = cursor.execute(query)
# viewOutput = viewResult.fetchall()
# print(viewOutput)

conn.commit()   # finalize inserted data
conn.close()