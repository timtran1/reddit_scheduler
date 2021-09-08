import sqlite3
from flask import Flask, send_from_directory, request
from dict_factory import dict_factory
import json

app = Flask(__name__)
with sqlite3.connect("database.db") as con:
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS post
               (title text, selftext text, subreddit text, schedule_date text, status text)''')


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


@app.route('/posts')
def posts():
    with sqlite3.connect("database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT rowid,* FROM post")
        return json.dumps(cur.fetchall())


@app.route('/posts/create')
def posts_create():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO post (status)"
            "VALUES ('Scheduled')"
        )
        return '1'


@app.route('/posts/update')
def posts_update():
    id = request.args.get('id')
    vals = json.loads(request.args.get('vals'))
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()

        for field in vals.keys():
            query = "UPDATE post SET %s = '%s' WHERE rowid = %s;" % (field, vals[field], id)
            # print(query)
            cur.execute(
                query
            )

    return '1'


@app.route('/posts/delete')
def posts_delete():
    id = request.args.get('id')
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM post WHERE rowid = %s" % id
        )

    return '1'


app.run(host='0.0.0.0')
