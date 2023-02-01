# -*- coding: utf-8 -*-
"""JJ_NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IWyaIwfTp6gyv5ZmEdkAI3tRyd8IP0zK
"""

import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

df= pd.read_json("/content/drive/MyDrive/train_set.json")

len(df)

type(df)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

df['data'][1]

type(df['data'][0])

df['data'][0]["summary"]

df['data'][2]

for i in range(len(df)):
  del df['data'][i]['article']

df['data'][500]

import json
from pandas import json_normalize

!pip install spacy==2.3.5

import spacy

!python -m spacy download en_core_web_sm

import spacy

len(df)

# df['data']

df['data'][0]['summary']

print(len(df))

print(len(df['data']))

import pandas as pd

# List of dictionaries with 110000 values
data = df['data']

# Create a dataframe with columns for 'summary', 'stock', and 'date'
df = pd.DataFrame(columns=['summary', 'stock', 'date'])

# Add each value as a new row in the dataframe
for i, d in enumerate(data):
    df.loc[i] = [d['summary'], d['stock'], d['date']]

# Print the dataframe
print(df)

df.head()

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download("vader_lexicon")

df['stock'].unique()

!pip install vaderSentiment

"""# Correct"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object
    sid_obj = SentimentIntensityAnalyzer()
    # polarity_scores method of SentimentIntensityAnalyzer object gives a sentiment dictionary 
    sentiment_dict = sid_obj.polarity_scores(sentence)


    sentiment = ""
    # Decide sentiment as very bullish, slightly bullish, neutral, very bearish or slightly bearish
    if sentiment_dict['compound'] >= 0.5 :
        sentiment = "Very Bullish"
    elif sentiment_dict['compound'] >= 0.05 :
        sentiment = "Slightly Bullish"
    elif sentiment_dict['compound'] <= - 0.5 :
        sentiment = "Very Bearish"
    elif sentiment_dict['compound'] <= - 0.05 :
        sentiment = "Slightly Bearish"
    else :
        sentiment = "Neutral"
    return sentiment
    
df['sentiments'] = df['summary'].apply(lambda x: sentiment_scores(x))

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object
    sid_obj = SentimentIntensityAnalyzer()
    # polarity_scores method of SentimentIntensityAnalyzer object gives a sentiment dictionary 
    sentiment_dict = sid_obj.polarity_scores(sentence)


    # sentiment = ""
    # # Decide sentiment as very bullish, slightly bullish, neutral, very bearish or slightly bearish
    # if sentiment_dict['compound'] >= 0.5 :
    #     sentiment = "Very Bullish"
    # elif sentiment_dict['compound'] >= 0.05 :
    #     sentiment = "Slightly Bullish"
    # elif sentiment_dict['compound'] <= - 0.5 :
    #     sentiment = "Very Bearish"
    # elif sentiment_dict['compound'] <= - 0.05 :
    #     sentiment = "Slightly Bearish"
    # else :
    #     sentiment = "Neutral"
    return sentiment_dict['compound']
    
df['scores'] = df['summary'].apply(lambda x: sentiment_scores(x))

df.head()

df.dropna()

len(df)

# sort the data by the sentiment column in descending order
df = df.sort_values(by="sentiments", ascending=False)

# reset the index of the DataFrame
df = df.reset_index(drop=True)

# view the first few rows of the sorted data
df.head()

# create a list of dictionaries from the data
predictions = [{"id": index, "summary": row["summary"]} for index, row in df.iterrows()]
rankings = [{"ticker": row["stock"], "rank": row["scores"]} for index, row in df.iterrows()]

# create the final dictionary
result = {
    "predictions": predictions,
    "rankings": rankings
}

# view the final dictionary
print(result)

result

import json
with open("predictions.json", "w") as outfile:
    json.dump(result, outfile)

