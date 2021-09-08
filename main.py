import sqlite3
from flask import Flask, send_from_directory, request
from dict_factory import dict_factory
import json
import logging

app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


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
            cur.execute(
                'UPDATE post SET %s = :value WHERE rowid = :id' % field,
                {
                    'value': vals[field],
                    'id': id
                }
            )

    return '1'


@app.route('/posts/delete')
def posts_delete():
    id = request.args.get('id')
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM post WHERE rowid = ?", (id)
        )

    return '1'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)  # dev server only
