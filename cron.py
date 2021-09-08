import sqlite3
import datetime
from dict_factory import dict_factory
import traceback
import praw
import os

now = datetime.datetime.now()
print('Checking posting schedule - %s' % str(now))

with sqlite3.connect("database.db") as con:
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT rowid,* FROM post WHERE status != 'Submitted' ")
    posts = cur.fetchall()

if posts:
    reddit = praw.Reddit(
        client_id=os.environ.get('CLIENT_ID'),
        client_secret=os.environ.get('CLIENT_SECRET'),
        user_agent=os.environ.get('USER_AGENT'),
        username=os.environ.get('USERNAME'),
        password=os.environ.get('PASSWORD')
    )

    for post in posts:
        try:
            if post['schedule_date']:
                schedule_date = datetime.datetime.strptime(post['schedule_date'], '%Y-%m-%dT%H:%M')
                if now > schedule_date:
                    print('SUBMITTING "%s"' % post['title'])
                    subreddit = reddit.subreddit(post['subreddit'])
                    subreddit.submit(
                        title=post['title'],
                        selftext=post['selftext']
                    )

        except Exception:
            print(post)
            print(traceback.format_exc())

else:
    print('No posts found.')
