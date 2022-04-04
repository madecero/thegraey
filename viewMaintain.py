# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 15:34:08 2022
viewMaintain
@author: de0
"""

import sqlite3
import os

#TODO: Change to a local directory you want to store the raw txt files
os.chdir(r'<INSERT PATH>')

conn = sqlite3.connect('de0project.db') # open the connection
cursor = conn.cursor()

#dropViews
dropDeleteView = 'DROP VIEW deleteView;'

dropHashView = 'DROP VIEW HashTags;'

cursor.execute(dropDeleteView)
cursor.execute(dropHashView)

#create views

deleteView = '''
CREATE VIEW deleteView AS
SELECT
    TD.ID,
    TD.UserID,
    TD.Text,
    TD.CreatedAt,
    DD.deleteReason
FROM TweetData TD LEFT OUTER JOIN deletedData DD
ON TD.ID = DD.tweetID;
'''

view = '''
CREATE VIEW HashTags AS
SELECT
    HD.HashTag,
    DD.deleteReason,
    DD.CreatedAt
FROM HashtagData HD LEFT OUTER JOIN deleteView DD
ON HD.TweetID = DD.ID;
'''

cursor.execute(deleteView)
cursor.execute(view)


conn.commit()   # finalize inserted data
conn.close()    # close the connection
