# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 12:40:22 2022
Queries+Analysis
@author: madec
"""

import sqlite3
import os
from wordcloud import WordCloud, STOPWORDS
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language

# #nlp to determine the word is english
# @Language.factory('language_detector')
# def language_detector(nlp, name):
#     return LanguageDetector()

# nlp = spacy.load("en_core_web_sm")
# nlp.add_pipe('language_detector', last=True)

#TODO: Change to a local directory you want to store the raw txt files
os.chdir(r'C:\Users\madec\Documents\de0project')

conn = sqlite3.connect('de0project.db') # open the connection
cursor = conn.cursor()

#open file to write to
writefile = open('censoredtweets.txt', 'w',encoding="utf-8")

#all_tweets_count
allTweetsCount = '''
SELECT COUNT(*)
FROM TweetData
;
'''

viewResult = cursor.execute(allTweetsCount)
viewOutput = viewResult.fetchall()
print (viewOutput)

#deleted_tweets_count
deletedTweetsCount = '''
SELECT COUNT(*)
FROM deleteView
;
'''

viewResult = cursor.execute(deletedTweetsCount)
viewOutput = viewResult.fetchall()
print (viewOutput)

#deleted_summary
deletedByCodeCount = '''
SELECT deleteReason, COUNT(*)
FROM deletedData
WHERE 
deleteReason = 'Twitter API returned a 403 (Forbidden), Sorry, you are not authorized to see this status.'
OR
deleteReason = 'Twitter API returned a 403 (Forbidden), User has been suspended.'
OR
deleteReason = 'Twitter API returned a 404 (Not Found), No status found with that ID.'
OR
deleteReason = 'Twitter API returned a 404 (Not Found), Sorry, that page does not exist.'
OR
deleteReason = 'Twitter API returned a 404 (Not Found), This Tweet is no longer available because it violated the Twitter Rules.'
OR
deleteReason = 'Twitter API returned a 404 (Not Found), This Tweet is no longer available.'
GROUP BY deleteReason
;
'''

viewResult = cursor.execute(deletedByCodeCount)
viewOutput = viewResult.fetchall()
for i in viewOutput:
    print (i)

#the following queries are commented out - they are only here for reference refer to the query_for_wordclouds+wordcounts section to continue

#violated tweets
violatedTweets = '''
SELECT Name, ScreenName, CreatedAt, TEXT
FROM deleteView
WHERE deleteReason = 'Twitter API returned a 404 (Not Found), This Tweet is no longer available because it violated the Twitter Rules.'
ORDER BY ID DESC
;
'''

# viewResult = cursor.execute(violatedTweets)
# viewOutput = viewResult.fetchall()
# for i in viewOutput:
#     writefile.write('\n\n')
#     writefile.write(str(i[0]) + '\n')
#     writefile.write(str(i[1]) + '\n')
    
#deletedURLs
# deletedURLs = '''
# SELECT URL
# FROM URLData UD
# INNER JOIN deletedData DD ON UD.TweetID = DD.tweetID
# WHERE deleteReason IS NOT NULL
# AND URL IS NOT NULL
# LIMIT 20
# ;
# '''

# viewResult = cursor.execute(deletedURLs)
# viewOutput = viewResult.fetchall()
# for i in viewOutput:
#     print (i)

#query_for_wordclouds+wordcounts
# query = '''
# SELECT ScreenName
# FROM UserData
# WHERE ScreenName = 'charliekirk11'
# ;
# '''

#print results of query
viewResult = cursor.execute(violatedTweets)
viewOutput = viewResult.fetchall()
for i in viewOutput:
    writefile.write('\n\n\n' + '**' + str(i[0]) + '**' + '     ' + '@' + str(i[1]) + '  -  '  + str(i[2]) + '\n')
    writefile.write(str(i[3]))

# # #write to a file for a wordcloud to reference
# file = open('suspendedTweets.txt', 'w', encoding="utf-8", newline = '')

# # for i in viewOutput:
# #     file.write(str(i) + '\n')

# # file.close()

# for i in viewOutput:
#     for k in i:
#         text = str(k)
#         doc = nlp(text)
#         detect_language = doc._.language
#         if detect_language['language'] == 'en':
#             file.write(str(k) + ' ')

# file.close()

# #exlude words we don't care about
# stopWords = set(STOPWORDS)
# customList = ['RT', 't', 'co', 'u', 'retweet', 'one', 'now', 's', 'm', 'dm', 'will', 'end', 'https', 'ur', 'etc', 'amp',
#               'n', 'nhttps']

# for i in customList:
#     stopWords.add(i)

# #read in file for wordcloud
# file = open('suspendedTweets.txt', 'r', encoding="utf-8", newline = '')
# text = file.read()
# textList = text.split()
# file.close()

# #wordcloud image
# word_cloud = WordCloud(background_color = 'white', max_words = 23, stopwords = stopWords).generate(text)
# img = word_cloud.to_image()
# img.show()

# #generate word counts
# hashTable = {}
# for word in textList:
#     if word.lower() not in stopWords:
#         if word.lower() not in hashTable:
#             hashTable[word.lower()] = 1
#         else:
#             hashTable[word.lower()] += 1

# tuplesList = sorted(hashTable.items(), reverse = True, key = lambda x: x[1])
# newList = []
# for i in tuplesList:
#     newList.append((i[0], i[1]))
# for t in newList[:100]:
#     print (t)

writefile.close()
conn.commit()   # finalize inserted data
conn.close()    # close the connection