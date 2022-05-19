# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:21:10 2021

@author: de0
"""

import sqlite3
import os

os.chdir(os.getcwd())

conn = sqlite3.connect('de0project.db') # open the connection
cursor = conn.cursor()

# Clean up and drop tables
cursor.execute('DROP TABLE UserData')
cursor.execute('DROP TABLE TweetData')
cursor.execute('DROP TABLE HashtagData')
cursor.execute('DROP TABLE MediaData')
cursor.execute('DROP TABLE URLData')
cursor.execute('DROP TABLE deletedData')

#Create table variables

createUserTable = '''
CREATE TABLE UserData
(
  ID VARCHAR2(25),
  Name VARCHAR2(50),
  ScreenName VARCHAR2(50),
  CreatedAt DATE,
  Description VARCHAR2,
  FollowersCount NUMBER,
  Location VARCHAR2,
  Verified BOOLEAN,
  
  PRIMARY KEY (ID)
);
'''

createTweetTable = '''
CREATE TABLE TweetData
(
  CreatedAt DATE,
  ID VARCHAR2(25),
  Text VARCHAR(285),
  InReplyToUserId VARCHAR(25),
  InReplyToScreenName VARCHAR2(50),
  InReplyToStatusID VARCHAR2(25),
  IsSensitive BOOLEAN,
  UserID VARCHAR(25),
  
  PRIMARY KEY (ID),
  
  FOREIGN KEY (UserID)
      REFERENCES UserData (ID)
);
'''

#Will pull from 'entities' key
#hashtags
createHashtagTable = '''
CREATE TABLE HashtagData
(
  TweetID VARCHAR2(25),
  HashTag VARCHAR(285),
 
  FOREIGN KEY (TweetID)
      REFERENCES TweetData (ID)
  );
'''

#media media: media_url
createMediaTable = '''
CREATE TABLE MediaData
(
  TweetID VARCHAR2(25),
  MediaURL VARCHAR2,
 
  FOREIGN KEY (TweetID)
      REFERENCES TweetData (ID)
  );
'''

#entities: urls
createURLTable = '''
CREATE TABLE URLData
(
  TweetID VARCHAR2(25),
  URL VARCHAR2,
 
  FOREIGN KEY (TweetID)
      REFERENCES TweetData (ID)
  );
'''

#table for deleted tweet reason codes
createDeletedTable = '''
CREATE TABLE deletedData
(
  tweetID VARCHAR2(25),
  userID VARCHAR2(25),
  deleteReason TEXT,
  
  PRIMARY KEY (tweetID),
  
  FOREIGN KEY (tweetID)
      REFERENCES TweetData (ID),
      
  FOREIGN KEY (userID)
      REFERENCES UserData (ID)
);
'''

#Create Tables
cursor.execute(createUserTable)
cursor.execute(createTweetTable)
cursor.execute(createHashtagTable)
cursor.execute(createMediaTable)
cursor.execute(createURLTable)
cursor.execute(createDeletedTable)

conn.commit()   # finalize inserted data
conn.close()    # close the connection
