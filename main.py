import csv
import tweepy
import os
import time




def twitter_authentification():
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("SECRET_CONSUMER_KEY"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("SECRET_TOKEN"),
        bearer_token=os.getenv("BEARER")
    )
    print("token", client.bearer_token)
    return client


def pick_a_website():
    with open('litterature_numerique.tsv', "r", newline='\n', encoding="UTF-8") as csvfile:
        dictreader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
        data_litte = list(dictreader)
    with open('tweeted_litt_num.tsv', "r", newline='\n', encoding="UTF-8") as csvfile:
        dictreader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
        already_twitted = list(dictreader)
        if not already_twitted:
            already_twitted = []
    i = 0
    workpiece = data_litte[i]
    if already_twitted:
        for a_t in already_twitted:
            if a_t["URL"] == workpiece["URL"]:
                i = i+1
                if i > len(already_twitted)-1:
                    return "Tout a déjà été twitté"
                workpiece = data_litte[i]
            else:
                return workpiece
    else:
        return workpiece
    return "Liste tweeted vide"

def create_tweet_content(workpiece):
    tweet_content = f"""{workpiece["Nom d'utilisateur"][:23]} nous a partagé {workpiece['URL']}, une oeuvre de littérature web ! Vous aussi partagez vos coups de coeur du web litteraire et participez à cultiver ce bot : https://framaforms.org/litterature-numerique-1647949367"""
    return tweet_content

def post_tweet(client, tweet_content):
    client.create_tweet(text=tweet_content)

def create_tweet_response(workpiece):
    if workpiece["Description"]:
        tweet_response = f"""{workpiece["Nom ou pseudo"][:23]} : {workpiece["Description"]}"""
        return tweet_response
    else:
        return None
def post_response(client, response):
    # id de BotEtRatures : 1507282224890232839
    time.sleep(4)
    get_tweets = client.get_users_tweets(id=1507282224890232839)
    print(list(get_tweets))
    id = get_tweets[3]["newest_id"]
    print(id)
    client.create_tweet(in_reply_to_tweet_id=id, text=response)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = twitter_authentification()
    workpiece = pick_a_website()
    tweet_content = create_tweet_content(workpiece)
    post_tweet(client, tweet_content)
    response = create_tweet_response(workpiece)
    if response:
        post_response(client, response)
