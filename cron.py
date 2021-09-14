import sqlite3
import datetime
from dict_factory import dict_factory
import traceback
import praw
import os
from tzlocal import get_localzone

now = datetime.datetime.now().astimezone(get_localzone())
print('Checking posting schedule - %s' % str(now))

with sqlite3.connect("database.db") as con:
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT rowid,* FROM post WHERE status != 'Submitted' ")
    posts = cur.fetchall()
    print('%s scheduled posts found.' % str(len(posts)))

if posts:
    reddit = praw.Reddit(
        client_id=os.environ.get('CLIENT_ID'),
        client_secret=os.environ.get('CLIENT_SECRET'),
        user_agent=os.environ.get('USER_AGENT'),
        username=os.environ.get('USERNAME'),
        password=os.environ.get('PASSWORD')
    )
    reddit.validate_on_submit = True

    for post in posts:
        try:
            if post['schedule_date']:
                schedule_date = datetime.datetime.strptime(post['schedule_date'], '%Y-%m-%dT%H:%M').astimezone(get_localzone())
                print('Post "%s" is scheduled for %s.' % (post['title'], str(schedule_date)))
                if now > schedule_date:
                    print('SUBMITTING "%s"' % post['title'])

                    if not os.environ.get('DEV_ENV'):
                        subreddit = reddit.subreddit(post['subreddit'])
                        subreddit.submit(
                            title=post['title'],
                            selftext=post['selftext'] or ' '
                        )

                        with sqlite3.connect("database.db") as con:
                            cur = con.cursor()
                            cur.execute(
                                "UPDATE post SET status = 'Submitted' WHERE rowid = %s;" % post['rowid']
                            )

            else:
                print('Post "%s" does not have a date.' % post['title'])

        except Exception:
            print(post)
            print(traceback.format_exc())
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE post SET status = 'Error' WHERE rowid = %s;" % post['rowid']
                )
