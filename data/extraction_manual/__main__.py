from credentials import *
from tweets_collection import *
from user_tweets import *

keywords = get_keywords()
print(keywords)

for k in keywords :
        k_tweets = collect(k)
        store_tweets(k_tweets, k)
        #for first two users
        for i in range(2):
            user_id = k_tweets[i]['user']['id']
            user_id_str = k_tweets[i]['user']['id_str']
            user_tweets = collect_by_user(user_id)
            store_user_tweets(user_tweets, k, user_id_str)