# -*- coding: utf-8 -*-
"""
Created on Thu May 26 12:30:37 2022
streamlitWork
@author: madec
"""

import streamlit as st

VERSION = "1.0"

st.set_page_config(
    page_title="CensoredTweets",
    page_icon="twitterBanned.png",
)

#SIDEBAR
with st.sidebar:
    st.header("Censored Tweets!")
    st.image("twitterBanned.png")
    st.info(
        "The tweets you see on this page have been deleted by Twitter for violating the [rules](https://help.twitter.com/en/rules-and-policies/twitter-rules) of their platform.\n\n"
        "I do not condone hate speech. The purpose of this page is to inform the public of what Twitter is deeming to be unacceptable for thier platform.\n\n"
        "Reader discretion is strongly advised.\n\n\n\n"
        "To learn more, check out my blog: [inthegraey.com](https://inthegraey.com)")

tweetfile = open('censoredtweets.txt', 'r', newline='',encoding="utf-8")

for i in tweetfile:
    st.write(str(i) + '\n')

tweetfile.close()
