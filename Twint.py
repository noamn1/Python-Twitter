import twint
import sqlite3
from flask import Flask, json, send_file, render_template

app = Flask(__name__)
from multiprocessing import Process
from dotenv import load_dotenv
load_dotenv()
import os

def get_followers(name):
    c = twint.Config()
    c.Username = name
    #c.Custom = ["username", "tweets"]
    #c.User_full = True
    c.Database = 'followers.db'
    c.Store_json = True
    c.Output = "followers.json"
    #c.Format = ""

    twint.run.Followers(c)
    return True

def get_all_tweets(name):
    # Configure
    c = twint.Config()
    c.Username = name
    c.Database = 'twitter.db'
    #c.Store_json = True
    #c.Output = "twint.json"
    # c.Search = "pineapple"
    # c.Format = "Tweet id: {id} | Tweet: {tweet}"

    # c.Format = "Username: {username}"
    # a = twint.run.Followers(c)

    c.Format = "Tweet id: {id} |  Tweet: {tweet} | replies: {replies} | retweets: {retweets}"
    twint.run.Search(c)
    return True


def _formatResponse(replies, retweets, followers, tweets_count):
    return {"replies": replies, "retweets": retweets, "followers": followers, "tweets_count": tweets_count}


def get_followers_count(cursor):
    cursor.execute("SELECT count(user) FROM followers_names")
    followers = 0
    for row in cursor.fetchall():
        followers = row[0]
        break
    return followers

def get_tweets_count(cursor):
    cursor.execute("SELECT count(tweet) FROM tweets")
    tweets_count = 0
    for row in cursor.fetchall():
        tweets_count = row[0]
        break
    return tweets_count

def get_replies(cursor):
    cursor.execute("SELECT  replies, tweet FROM tweets  order by replies desc limit 5")
    replies = []
    for row in cursor.fetchall():
        replies.append({"replies": row[0], "tweet": row[1]})

    return replies

def get_retweets(cursor):
    cursor.execute("SELECT  retweets, tweet FROM tweets  order by retweets desc limit 5")
    retweets = []
    for row in cursor.fetchall():
        retweets.append({"retweets": row[0], "tweet": row[1]})
    return retweets

@app.route('/')
def get_twitter_data():
    username = os.getenv("TWITTER_NAME")

   # p = Process(target=get_all_tweets, args=(username,))
   # p.start()
  #  p.join()

   # p2 = Process(target=get_followers, args=(username,))
   # p2.start()
   # p2.join()

    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()

   # c.execute("SELECT name FROM sqlite_master WHERE type='table';")
   # for table in c.fetchall():
     #   print(table)

    retweets = get_retweets(c)
    replies = get_replies(c)
    tweets_count = get_tweets_count(c)

    conn = sqlite3.connect('followers.db')
    c = conn.cursor()
    followers = get_followers_count(c)

    resp = _formatResponse(replies, retweets, followers, tweets_count)
    return json.dumps(resp)

if __name__ == '__main__':
    app.run()





