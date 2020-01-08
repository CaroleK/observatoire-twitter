from tweets_collection import *

def collect_by_user(user_id):
    user_json_tweets = []
    connexion = twitter_setup()
    statuses = connexion.user_timeline(id = user_id, count = 200)
    for status in statuses:
        #print(status.text)
        user_json_tweets.append(status._json)
    return user_json_tweets


