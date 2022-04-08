import csv
import tweepy
import os
import time
from datetime import date
from random import randint

FIRST_DAY = date(2022, 0o4, 0o1)

def twitter_authentification():
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("SECRET_CONSUMER_KEY"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("SECRET_TOKEN"),
        bearer_token=os.getenv("BEARER")
    )
    return client


def append_to_tweeted(work):
    with open("tweeted_litt_num.tsv", 'a+', newline='\n', encoding="UTF-8") as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(work)


def pick_a_website():
    with open('litterature_numerique.tsv', "r", newline='\n', encoding="UTF-8") as csvfile:
        dictreader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
        data_litte = list(dictreader)
    try:
        print((date.today() - FIRST_DAY).days)
        workpiece = data_litte[(date.today() - FIRST_DAY).days]
    except IndexError:
        print("Tout a déjà été twitté")
    return workpiece


def create_tweet_content(workpiece):
    append_to_tweeted([workpiece["URL"]])
    if workpiece["Nom ou pseudo"] == "weblitt":
        tweet_content_list = [f"""{workpiece['URL']} est l'oeuvre de littérature web du jour ! Vous aussi partagez vos coups de coeur du web et participez à cultiver ce bot : https://framaforms.org/litterature-numerique-1647949367""",
        f"""Connaissiez-vous {workpiece['URL']} ? Maintenant oui ! Si elle vous fait penser à un compte twitter, un site, une fanfic ... faites le savoir à ce bot : https://framaforms.org/litterature-numerique-1647949367""",
        f"""Allez jeter un coup d'oeil à {workpiece['URL']}, alors qu'en pensez-vous ? Partagez vos coups de coeurs littéraire avec ce bot sur https://framaforms.org/litterature-numerique-1647949367""",
        f"""Cliquez ici pour une petite pause littéraire : {workpiece['URL']}. Nous avons besoin de vous pour partager toujours plus de littérature sur ce réseau : https://framaforms.org/litterature-numerique-1647949367""",
        f"""Vous reprendez-bien un petit peu de littérature en ligne ? {workpiece['URL']} ? Et vous, que lisez-vous en ligne ? Faites le moi savoir : https://framaforms.org/litterature-numerique-1647949367"""]

        tweet_content = tweet_content_list[randint(0, 4)]

    else:
        tweet_content = f"""{workpiece['URL']} est l'oeuvre de littérature web du jour, partagée par {workpiece["Nom ou pseudo"][:23]}! 
        Vous aussi partagez vos coups de coeur du web litteraire et participez à cultiver ce bot : https://framaforms.org/litterature-numerique-1647949367"""
    return tweet_content


def post_tweet(client, tweet_content):
    client.create_tweet(text=tweet_content)


def create_tweet_response(workpiece):
    if workpiece["Description"]:
        tweet_response = f'"{workpiece["Description"]}", {workpiece["Nom ou pseudo"][:23]} '
        return tweet_response
    else:
        return None


def post_response(client, response):
    # id de BotEtRatures : 1507282224890232839
    time.sleep(60)
    get_tweets = client.get_users_tweets(id=1507282224890232839)
    id = get_tweets[3]["newest_id"]
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
