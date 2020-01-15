import pandas as pd
import numpy as np
import os
import csv

path = os.path.normpath(os.path.dirname(os.path.abspath(__file__))+"/../../data/extraction_twint/data_service_clients/")

def __load_data(filename):
    """
    returns all the data required for computing reply time : 
    id, conversation_id, datetime and username
    """
    df=pd.read_csv(path+"/raw/"+filename+".csv")
    df['datetime']=pd.to_datetime(df['date'] + ' ' + df['time'])
    df.drop(['date','time'], axis=1, inplace=True)
    return df

def __compute_reply_time(df, username):
    """
    Calculates the reply time from the brand account, removes all the brand account tweets and saves it in a new csv
    Output : dataframe with 2 columns (id and reply_time)
    """

    ##Filter brand tweets
    brand_tweets = df[df['username'] == username.lower()].filter(['conversation_id','datetime'])
    ##Remove brand tweets from the main df
    df = df[df['username'] != username.lower()].filter(['id','conversation_id','datetime'])

    ##Join the tables
    df=df.set_index('conversation_id').join(brand_tweets.set_index('conversation_id'), lsuffix='', rsuffix='_reply')
    ##computes reply time
    df['reply_time']=df['datetime_reply']-df['datetime']

    #remove negative reply_time
    df = df.loc[df['reply_time'].apply(lambda x: x.days>=0)]
    #keep only the smallest value
    df = df.groupby("id", as_index=False)["reply_time"].min().set_index('id')
    return df

def __create_complete_dataframe(username, original_data, reply_time, save_to_csv=False, filename=None):
    #removes replies from the brand
    df = original_data[original_data['username'] != username.lower()].set_index('id')
    #add reply time
    df['reply_time']=reply_time['reply_time']

    if save_to_csv:
        df.to_csv(path+"/with_reply_time/"+filename+".csv")
    return df

def create_reply_time(username, filename, save_to_csv=False):
    df=__load_data(filename)
    reply_time=__compute_reply_time(df,username)
    df=__create_complete_dataframe(username, df, reply_time, save_to_csv, filename)
    return df

def __load_csv(file):
    rows = []
    with open(file, newline='',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

def computes_all_reply_times():
    #Load csv with account names + filenames

    brands = __load_csv(os.path.normpath(path+"/brand_accounts.csv"))

    #computes the reply time for every brand, and store it in the appropriate file
    for brand in brands:
        if brand["username"].lower()=='wholefoods':
            create_reply_time(brand["username"], brand.get("filename"), save_to_csv=True)

if __name__=="__main__":
    ##COMPUTES ALL REPLY_TIMES
    computes_all_reply_times()
    
    ##ONLY A SPECIFIC BRAND
    #df=create_reply_time('wholefoods','wholefoods', True)