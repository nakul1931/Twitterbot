import tweepy
import wget
import time
import requests
consumer_key =" "
consumer_secret = " "
key = " "
secret  =" "

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
#api.update_status('SECOND Tweet from Bot')


FILE_NAME = "last.txt"


def readd(FILE_NAME):
    file = open(FILE_NAME,'r')
    id2 = int(file.read().strip())
    file.close()
    return id2

def last_seen(FILE_NAME,id2):
    file = open(FILE_NAME,'w')
    file.write(str(id2))
    file.close()
    return

def send_r(id,data):
    my_url = "http://35.173.150.151:5000/post"
    data = {
        "username": id,
        "tweet": data,
        # "image": open('test.png', 'rb')
    }
    r = requests.post(url=my_url, data=data)
    print(r)


def reply():

    tweets = api.mentions_timeline(readd(FILE_NAME),tweet_mode = 'extended')
    # media_files = set()
    # for status in tweets:
    #      media = status.entities.get('media', [])
    # if(len(media) > 0):
    #      media_files.add(media[0]['media_url'])
    #      for media_file in media_files:
    #          wget.download(media_file)
    for tweet in reversed(tweets):
        if '#chandigarhpolice' or '#crime' or '#pcr' in tweet.full_text.lower():

            # tweet_data = tweet.text
            # print(tweet_data)
            status = api.get_status(tweet.id, tweet_mode="extended")
            try:
                mehanat = status.retweeted_status.full_text
                print(mehanat)
            except AttributeError:  # Not a Retweet
                mehanat = status.full_text
                print(mehanat)
                print(type(mehanat))
            print("replied to " + str(tweet.id))
            api.update_status("@" + tweet.user.screen_name + " Thanks for informing us! We will get back to you soon. ",tweet.id)
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)
            last_seen(FILE_NAME,tweet.id)
            new_id=str(tweet.user.screen_name)
            mehanat=str(mehanat)
            send_r(new_id,mehanat)

while True:
    reply()

    time.sleep(60)
    print("Working.....")
