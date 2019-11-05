# -*- coding: utf-8 -*-
import hashlib
import datetime
import redis
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import news_api_client

from cloudAMQP_client import CloudAMQPClient # pylint: disable=E0401, C0413

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3
SLEEP_TIME_IN_SECONDS = 10

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://nfdiqtrj:91N2aiPAipzdKvN-JoiP-B8Mjj09qSes@otter.rmq.cloudamqp.com/nfdiqtrj'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'tap-news-scrape-news-task-queue'

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)

    num_of_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

        if redis_client.get(news_digest) is None:
            num_of_news += 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            redis_client.set(news_digest, "True")
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)


            cloudAMQP_client.sendMessage(news) # send to rabbitmq

    print ("Fetched %d news." % num_of_news)

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)