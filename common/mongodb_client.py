# -*- coding: utf-8 -*-
# 自动管理连接时间
from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = 27017

DB_NAME = 'tap-news'

client = MongoClient("%s:%d" % (MONGO_DB_HOST, MONGO_DB_PORT))

def get_db(db=DB_NAME):
    return client[db]