# _*_ encoding:utf-8 _*_
# all the imports
import os
import sys
import sqlite3
import MySQLdb
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='root'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


#
#
# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
#
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
#
#
# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
#
# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print('Initialized the database.')
def connectdb():
    try:
        global conn
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='common', charset="utf8")
    except Exception as e:
        print e
        sys.exit()


def cursordb():
    global cursor
    cursor = conn.cursor()


def closedb():
    conn.close()
    cursor.close()


@app.route('/')
def show_entries():
    connectdb()
    cursordb()
    sql = "SELECT title, text FROM entries ORDER BY id DESC"
    cursor.execute(sql)
    entries = cursor.fetchall()
    closedb()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    connectdb()
    cursordb()
    try:
        sql = "INSERT INTO entries (title, text) VALUES ('%s','%s')" % (request.form['title'], request.form['text'])
        cursor.execute(sql)
    except Exception as e:
        print e
        print '这儿错了'
    conn.commit()
    closedb()
    flash('文章发布成功')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = '用户名错误'
        elif request.form['password'] != app.config['PASSWORD']:
            error = '密码错误'
        else:
            session['logged_in'] = True
            flash('登录成功')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('已退出登录')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)
