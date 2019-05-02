from db_connection import connect
from aws_sentiment import sentiment
from spell_checker import Spell_checker
import matplotlib.pyplot as plt
import pylab as pl
import tweepy

consumer_key = "lALVbQZLLl9QOvJ088VwvKLHC"
consumer_key_secret = "OQuQ7QnZTm4UH2CXCLfwwCw0eLzDOLJwakuJkVvMIMALpcBtoo"
access_token = "1315602882-IVRGBsGqtAciN4Mj8qBa5CWKJN185eDU5I6cMpq"
access_token_secret = "a0s2KxBC5WRkWOHKYTFMY23VnKAAfn2IOxhhBz7AOlhA4"

def auth(key, secret, token, token_secret):
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)
    return auth

def ask_search():
    tmp_searchs = []
    count = 0
    while(count<10):
        topic = input("Ingresa busqueda (N): ")
        if(topic == 'N'):
            break
        else:
            tmp_searchs.append(topic)
        count+=1
    return tmp_searchs

def graph_search(search, index_search, axes):
    positive_tweets = collection.find({"search" : search, "sentiment": "POSITIVE"})
    negative_tweets = collection.find({"search" : search, "sentiment": "NEGATIVE"})

    left = [1, 2]

    height = [collection.count_documents({"search" : search, "sentiment": "POSITIVE"}),
                collection.count_documents({"search" : search, "sentiment": "NEGATIVE"})]

    tick_label = ["POSITIVE","NEGATIVE"]
    axes[index_search,0].bar(left, height, tick_label = tick_label, color = ['green','red'])
    axes[index_search,0].set_title(f"Serach: {search} - By sentiment")


    date_score={}

    getnumby_date(date_score, positive_tweets, "POSITIVE")
    getnumby_date(date_score, negative_tweets, "NEGATIVE")

    colors = ['green','red']
    count = 0
    for label in tick_label:
        y = get_y(date_score,label)
        axes[index_search,1].plot_date(list(date_score.keys()),y, color = colors[count])
        count+=1

    axes[index_search,1].set_title(f"Serach: {search} - By Date")

def get_y(date_score,string):
    y = []
    for key in list(date_score.keys()):
        if(string in date_score[key]):
            y.append(date_score[key][string])
        else:
            y.append(0)
    return y


def getnumby_date(library, collection, string):
    for tweet in collection:
        if(tweet["date"] in library):
            if( string in library[tweet["date"]]):
                library[tweet["date"]][string]= library[tweet["date"]][string]+1
            else:
                library[tweet["date"]][string] = 1
        else:
            library[tweet["date"]] = {}
            library[tweet["date"]][string] = 1





if __name__ == '__main__':

    auth = auth(
    consumer_key,
    consumer_key_secret,
    access_token,
    access_token_secret
    )

    api  = tweepy.API(auth)

    collection = connect()

    searchs = ask_search()

    Spell_checker = Spell_checker()

    fig, axes = plt.subplots(len(searchs), 2)
    index_search = 0
    for search in searchs:
         print(f"Obteniendo los tweets de {search}")
         tmp_tweets = []
         num_tweets = 0
         for tweet in  tweepy.Cursor(api.search,q=search,lang="es",tweet_mode="extended").items(100):
              decoded = tweet._json
              text = decoded["full_text"]
              date = tweet.created_at.date()

              if(text[0:2] == "RT" or collection.count_documents({"id": tweet.id,"search" : search }) > 0):
                  continue

              clean_tweet = Spell_checker.filter(text)

              query = {"id": tweet.id,
                      "search" : search,
                      "date": date.isoformat(),
                      "text": clean_tweet,
                      "sentiment": sentiment(clean_tweet)}

              collection.insert_one(query)
              num_tweets+=1

         print(f"Tweets guardados: {num_tweets}")
         graph_search(search, index_search, axes)
         index_search+=1
    plt.show()
