# _*_ encoding:utf-8 _*_
# all the imports
import sys

from flask import Flask, request, session, redirect, url_for, abort, \
    render_template, flash
from sqlalchemy import Table, Column, Integer, String, select, create_engine, MetaData

from config import conn
from models import news

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

engine = create_engine("mysql://root:root@localhost:3306/common?charset=utf8", encoding="utf-8", echo=True)
metadata = MetaData()

# 定义表
news = Table('news', metadata,
             Column('id', Integer, primary_key=True),
             Column('title', String(128)),
             Column('text', String(1280)),
             )

# 创建数据表，如果数据表存在，则忽视
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()


@app.route('/')
def show_entries():
    s = select([news.c.title, news.c.text]).order_by(news.c.id.desc())
    result = conn.execute(s)
    entries = result.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    i = news.insert()
    u=dict(title=request.form['title'], text=request.form['text'])
    result = conn.execute(i, **u)
    result.inserted_primary_key
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
