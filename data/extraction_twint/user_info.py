import pandas as pd
import numpy as np
import os
import csv
import twint

path = os.path.normpath(os.path.dirname(os.path.abspath(__file__))+"/../../data/extraction_twint/tweets_data/data_service_clients/")

def __load_data(filename):
    """
    returns all the data required for computing reply time : 
    id, conversation_id, datetime and username
    """
    df=pd.read_csv(path+"/with_reply_time/"+filename+".csv")
    return df

def __load_csv(file):
    """Loads the csv file containing all the brands names that should be extrated
    returns a list of dictionnaries :
    [
        {'account': '@AmazonHelp', 'filename': 'amazon'},
        {'account', '@StarbucksHelp', 'filename': 'starbucks')
    ]
    """
    rows = []
    with open(file, newline='',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


# def __create_complete_dataframe(username, original_data, reply_time, save_to_csv=False, filename=None):
#     #removes replies from the brand
#     df = original_data[original_data['username'] != username[1:].lower()].set_index('id')
#     #add reply time
#     df['reply_time']=reply_time['reply_time']

#     if save_to_csv:
#         df.to_csv(path+"/with_user_info/"+filename+".csv")
#     return df



def load_user_info(filename):
    """Load user info for all users in the df
    """
    df = __load_data(filename)
    users = df["username"].unique()
    len_users = len(users)

    for i in range(len_users):
        if i%100 == 0:
            print("{} : {}/{} users extracted".format(filename,i,len_users))
        get_user(users[i], filename)

def get_user(username, filename):
    c = twint.Config()
    filename = os.path.normpath(path+"/users_info/"+filename+".csv")
    c.Output = filename
    c.Store_csv = True
    c.Count = True
    c.Hide_output = True
    c.Username = username
    twint.run.Lookup(c)

def load_user_info_all_brands():
    #Load csv with account names + filenames
    brands = __load_csv(os.path.normpath(path+"/../../brand_accounts.csv"))

    #computes the reply time for every brand, and store it in the appropriate file
    for brand in brands:
        load_user_info(brand.get("filename"))

if __name__=="__main__":
    ##LOAD USER INFO FOR ALL BRANDS
    #load_user_info_all_brands()
    
    ##ONLY A SPECIFIC BRAND
    load_user_info('wholefoods')
