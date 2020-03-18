import pandas as pd
import numpy as np
import os
import csv
import twint

path = os.path.normpath(os.path.dirname(os.path.abspath(__file__))+"/../../data/extraction_twint/tweets_data/data_service_clients/")

def __load_databases(filename):
    """
    returns all the data required for computing reply time : 
    id, conversation_id, datetime and username
    """
    tweets = pd.read_csv(path+"/with_reply_time/"+filename+".csv")
    users = pd.read_csv(path+"/users_info/"+filename+".csv")

    #lowercase all ids
    tweets.username = tweets.username.apply(lambda x : x.lower())
    users.username = users.username.apply(lambda x : x.lower())
    return tweets, users

def join_databases(filename):
    #load databases
    tweets, users = __load_databases(filename)
    ##Join the tables
    tweets=tweets.join(users.set_index('username'),how='inner', on='username', lsuffix='', rsuffix='_user')
    tweets = tweets.set_index('id')
    #save to csv
    tweets.to_csv(path+"/with_user_info/"+filename+".csv")
    return tweets

if __name__=="__main__":
    ##ONLY A SPECIFIC BRAND
    #join_databases('wholefoods')

    tweets = join_databases('wholefoods')
    print(tweets.head())
