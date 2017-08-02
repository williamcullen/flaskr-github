# _*_ coding:utf-8 _*_
__author__ = 'williamcullen'
__date__ = '2017/7/6 9:54'

import os, sys, string
import MySQLdb
import flaskr


# # 连接数据库　
# try:
#     conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='common')
# except Exception as e:
#     print(e)
#     sys.exit()
#
# # 获取cursor对象来进行操作
# cursor = conn.cursor()
# # 创建表
# sql = "create table if not exists blog(name varchar(128) primary key, age int(4))"
# cursor.execute(sql)
# # 插入数据
# sql = "insert into blog(name, age) values ('%s', %d)" % ("zhaowei", 23)
# try:
#     cursor.execute(sql)
# except Exception as e:
#     print(e)
#
# sql = "insert into blog(name, age) values ('%s', %d)" % ("张三", 21)
# try:
#     cursor.execute(sql)
# except Exception as e:
#     print(e)
#
# # 插入多条
# sql = "insert into blog(name, age) values (%s, %s)"
# val = (("李四", 24), ("王五", 25), ("洪六", 26))
# try:
#     cursor.executemany(sql, val)
# except Exception, e:
#     print e
#
# # 查询出数据
# sql = "select * from blog"
# cursor.execute(sql)
# alldata = cursor.fetchall()
# # 如果有数据返回，就循环输出, alldata是有个二维的列表
# if alldata:
#     for rec in alldata:
#         print rec[0], rec[1]
#
# cursor.close()
# conn.close()

def connectdb():
    try:
        global conn
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='common')
    except Exception as e:
        print e
        sys.exit()


def cursordb():
    global cursor
    cursor = conn.cursor()
    return cursor


def closedb():
    conn.close()
    cursor.close()


if __name__ == '__main__':
    connectdb()
    cursordb()
    sql = "INSERT INTO entries(title, text) VALUES ('%s','%s')" % ('oooo', 'pppp')
    cursor.execute(sql)
    conn.commit()
    closedb()

    # conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='common')
    # cursor = conn.cursor()
    # sql = "INSERT INTO entries(title, text) VALUES ('oliver6', 'my name is  Olicer Queen')"
    # cursor.execute(sql)
    # conn.commit()
    # conn.close()
    # cursor.close()

    connectdb()
    cursor = cursordb()
    sql = "SELECT id,title, text FROM entries ORDER BY id DESC"
    cursor.execute(sql)
    entries = cursor.fetchall()
    print entries
    closedb()
