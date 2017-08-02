# _*_ encoding:utf-8 _*_
__author__ = 'williamcullen'
__date__ = '2017/8/2 11:34'

from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql://root:root@localhost:3306/common?charset=utf8", encoding="utf-8", echo=True)
metadata = MetaData()
# 创建数据表，如果数据表存在，则忽视
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
