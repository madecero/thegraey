# -*- coding: utf-8 -*-
"""
deletedTweetsdb
Created on Sat Jan 29 12:35:26 2022

@author: madec
"""

import os
import ast
import sqlite3

#TODO: Change to a local directory you want to store the raw txt files
os.chdir(r'INSERT PATH')

conn = sqlite3.connect('de0project.db') # open the connection
cursor = conn.cursor()

deletefile = open('deletedTweets_raw_FINAL.txt', 'r', encoding="utf-8")
num_lines = sum(1 for line in deletefile)
print ('number of tweets to review: ' + str(num_lines))
print ('\n')
deletefile.close()

deletefile = open('deletedTweets_raw_FINAL.txt', 'r', encoding="utf-8")
counter = 0

for i in range(num_lines):
    line = deletefile.readline()
    tweet = ast.literal_eval(line) # converts the string to a dictionary
    deleteList = []
    deleteList.append(tweet['id'])
    deleteList.append(tweet['user']['id'])
    deleteList.append(tweet['TwythonError'])

    cursor.execute("INSERT OR IGNORE INTO deletedData VALUES (?, ?, ?);", deleteList)
    counter += 1
    print ('number of tweets replicated: ' + str(counter))
    print ('\n')

deletefile.close()
conn.commit()   # finalize inserted data
conn.close()    # close the connection
