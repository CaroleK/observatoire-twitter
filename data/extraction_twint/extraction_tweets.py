import twint
import os
import csv
from threading import Thread, Lock
import numpy as np
import asyncio

path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

def load_csv(file):
    rows = []
    with open(file, newline='',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

class Search(Thread):
    def __init__(self, file, keyword=None, mention = None, to_username=None, from_username=None, allow_append=False, limit=None, user_info=None, members_list=None):
        self.file = file
        self.keyword = keyword
        self.mention = mention
        self.to_username = to_username
        self.from_username = from_username
        self.allow_append = allow_append
        self.limit = limit
        self.user_info = user_info
        self.members_list = members_list
        Thread.__init__(self)

    def run(self):
        print("New search launched : \n keyword: {}\n to: {}\n from: {}\n file:  {}\n".format(self.keyword, self.to_username, self.from_username, self.file))

        # création de l’objet twint
        c = twint.Config()
        # Critères de recherche
        c.Lang = "en"

        if self.keyword:
            c.Search = self.keyword
        if self.mention:
            c.All = self.mention
        if self.to_username:
            c.To = self.to_username
        if self.from_username:
            c.Username = self.from_username
        if self.limit:
            c.Limit = self.limit
        if self.user_info:
            c.User_full = True
        if self.members_list:
            c.Members_list = self.members_list

        ##Exemple of query : from WholeFoods to IIMiranda
        # c.To = "IIMiranda"
        # c.Username = "WholeFoods"

        # Champs à stocker dans le CSV
        # c.Custom["tweet"] = ["tweet"]

        c.Store_csv = True
        c.Count = True
        c.Hide_output = True
        c.Output = self.file

        if (not self.allow_append) and os.path.exists(self.file):
            print("Cancelled search : file already existing : {}".format(self.file))
        else:
            asyncio.set_event_loop(asyncio.new_event_loop())
            twint.run.Search(c)
            print("Search done")


def extract_service_clients_data(numberOfBrands, limitNumberOfTweets):
    #Load csv with account names + filenames
    brands = load_csv(path + '/brand_accounts.csv')

    #Launch a search for every brand, and store it in the appropriate file
    for i in range(numberOfBrands):

        #set up the search
        filename = path + "/tweets_data/data_service_clients/raw/" + brands[i].get("filename") + ".csv"
        search=Search(filename, mention=brands[i].get("account"), limit=limitNumberOfTweets)
        
        #start the search
        search.start()
    

def extract_marketing_personnalise_data(numberOfProducts,limitNumberOfTweets):
    
    # Load brands' name
    products = [product.get('product') for product in load_csv(path + '/product_keywords.csv')]
    
    #1. FIRST EXTRACTION : Tweets containing the brand
    first_extraction_thread = Thread(target=first_extraction_marketing_personnalise, args=(products, numberOfProducts,limitNumberOfTweets))
    
    #2. SECOND EXTRACTION : Users' tweets
    second_extraction_thread = Thread(target=second_extraction_marketing_personnalise, args=(products, numberOfProducts))

    # Launch threads one after another
    first_extraction_thread.start()
    first_extraction_thread.join()
    
    second_extraction_thread.start()
    second_extraction_thread.join()


def first_extraction_marketing_personnalise(products, numberOfProducts, limitNumberOfTweets):
    
    #Launch a search for every brand, and store it in the appropriate file
    searchs = []
    for i in range(numberOfProducts):
        #set up the search
        filename = path + '/tweets_data/data_marketing_personnalise/' + products[i] + '.csv'

        search=Search(filename, keyword=products[i], limit=limitNumberOfTweets, members_list=[products[i]])
        searchs.append(search)
        #start the search
        search.start()
    
    # Wait for all searches to finish
    for search in searchs:
        search.join()
    

def second_extraction_marketing_personnalise(products, numberOfProducts):

    for i in range(numberOfProducts):
        filename = path + '/tweets_data/data_marketing_personnalise/' + products[i] + '.csv'
       
        users  = [tweet.get('username') for tweet in load_csv(filename)]
        users_unique = get_unique(users)
       
        filename2 = path + '/tweets_data/data_marketing_personnalise/' + products[i] + "_users.csv"

        for user in users_unique :
            search_users_tweets=Search(filename2, from_username=user, limit=100)
            #start the search
            search_users_tweets.start()

def get_unique(a_list): 
    x = np.array(a_list)
    return np.unique(x)


if __name__=="__main__":

    #extract_service_clients_data(1, 200)
    extract_marketing_personnalise_data(1, 100)








