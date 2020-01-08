import tweepy
import json
import xlrd 
# We import our access keys:
from credentials import *   

def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with an access keys provided in a file credentials.py
    :return: the authentified API
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

def get_keywords():
    keywords_list = []
   
    wb = xlrd.open_workbook('product_keywords.xlsx') 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 
  
    for i in range(1, sheet.nrows): 
        keywords_list.append(sheet.cell_value(i, 0))

    return keywords_list
    


def collect(keyword):
    connexion = twitter_setup()
    tweets = connexion.search(keyword,lang="en",locale="english",rpp=100, show_user = True)
    json_tweets = []
    for tweet in tweets:
        json_tweets.append(tweet._json)
    return json_tweets

def store_tweets(tweets, filename):
    with open("tweets_data/" + filename + "/"+ filename + ".json", "w") as write_file:
        json.dump(tweets, write_file)

def store_user_tweets(tweets, keyword, filename):
    with open("tweets_data/" + keyword + "/"+ filename + ".json", "w") as write_file:
        json.dump(tweets, write_file)





