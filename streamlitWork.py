# -*- coding: utf-8 -*-
"""
Created on Thu May 26 12:30:37 2022
streamlitWork
@author: madec
"""

import streamlit as st

VERSION = "0.1"

st.set_page_config(
    page_title="CensoredTweets",
    page_icon="twitterbanned.png",
)

st.title("Censored Tweets! /n Reader discretion is strongly advised.")

tweetfile = open('censoredtweets.txt', 'r', newline='',encoding="utf-8")

for i in tweetfile:
    st.write(str(i) + '\n')

tweetfile.close()
