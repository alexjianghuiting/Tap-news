# -*- coding: utf-8 -*-
# 跟mongodb里的数据做deduplicate
import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
#import news_topic_modeling_service_client

from cloudAMQP_client import CloudAMQPClient

NEWS_TABLE_NAME = "news"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

SLEEP_TIME_IN_SECONDS = 3

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://nfdiqtrj:91N2aiPAipzdKvN-JoiP-B8Mjj09qSes@otter.rmq.cloudamqp.com/nfdiqtrj'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'tap-news-dedupe-news-task-queue'

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = task['text']
    if text is None:
        return

    # $lt $lte $gt $gte
    # < 、 <= 、 > 、 >=

    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt': {'$gte': published_at_day_begin,
                          '$lt': published_at_day_end}}))
    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        sim = tfidf * tfidf.T

        print(sim.A)

        rows, _ = sim.shape
        for row in range(1, rows):
            if sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print ('Duplicated news. Ignore.')
                return
    # mongodb要用时间做id
    # convert string to mongodb request data type
    task['publishedAt'] = parser.parse(task['publishedAt'])

    # Replaces a single document within the collection based on the filter
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)
    print("new news be added into mongodb")

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            # Parse the msg
            try:
                print("Parse and process the message")
                handle_message(msg)
                print("process finished")
            except Exception as e:
                print(e)
                pass

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)