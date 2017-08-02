# _*_ encoding:utf-8 _*_
__author__ = 'williamcullen'
__date__ = '2017/8/2 11:33'
from sqlalchemy import Table, Column, Integer, String

from config import metadata

# 定义表
news = Table('news', metadata,
             Column('id', Integer, primary_key=True),
             Column('title', String(128)),
             Column('text', String(1280)),
             )
