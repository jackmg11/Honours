
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
import praw
import requests
from praw.models import MoreComments
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


def sentimentAverage():
    reddit = praw.Reddit(client_id = "SBoMWoiu5uvPdg",
                        client_secret = "9cLsdjErIJovr4qb40kPoB9TmW-hPA",
                        username = "apiguy123",
                        password = "fatladonsteds123",
                        user_agent = "jack")


    headlines = []

    for submission in reddit.subreddit('CryptoCurrency').hot(limit=None):
        headlines.append(submission.title)
        
        #print(len(headlines))


    sia = SIA()
    results = []
    #print(headlines)

    for line in headlines:
        pol_score = sia.polarity_scores(line)
        pol_score['headline'] = line
        results.append(pol_score)

#pprint(results[1:50], width=100)

    complist = []
    for i in results:
        complist.append(i["compound"])
    total = 0
    for i in complist:
        total+= i
        print(total)
    #print(total/len(complist))
    av = np.average(complist)
    if av > 0.00 and av <0.5:
        return "Moderate Positivity"
    elif av > 0.5:
        return "Very Positive"
    elif av <0.00 and av > -0.5:
        return "Slightly Negativity"
    else:
        return "Very Negative"
print(sentimentAverage())