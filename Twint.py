import twint
from flask import Flask, json

app = Flask(__name__)
from multiprocessing import Process
import sqlite3


def f(name):
    # Configure
    c = twint.Config()
    c.Username = "Benbenfren"
    c.Limit = 60
    c.Database = 'twitter.db'
    # c.stats
    # c.Search = "pineapple"
    # c.Format = "Tweet id: {id} | Tweet: {tweet}"

    # c.Format = "Username: {username}"
    # a = twint.run.Followers(c)

    c.Format = "Tweet id: {id} |  Tweet: {tweet} | replies: {replies} | retweets: {retweets}"
    # a = twint.run.Profile(c)

    # Run
    a = twint.run.Search(c)

    print(a)
    return 'a'


@app.route('/')
def hello():
   # p = Process(target=f, args=('bob',))
   # p.start()
   # p.join()
    res = {}
    res['tweets'] = []
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in c.fetchall():
        print(table)
        cursor = c.execute('SELECT id, retweets, retweet, tweet, replies FROM tweets')
        # names = list(map(lambda x: x[0], cursor.description))
        # print(names)
        for result in c.fetchall():
            res['tweets'].append({"id": result[0], 'retweets': result[1], 'retweet': result[2], 'tweet': result[3]})

    return json.dumps(res)

if __name__ == '__main__':
    app.run()





