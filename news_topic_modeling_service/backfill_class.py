# labels the data that are already in the database
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import common.mongodb_client as mongodb_client
import common.news_topic_modeling_service_client as news_topic_modeling_service_client

if __name__ == '__main__':
    db = mongodb_client.get_db()
    cursor = db['news'].find({})
    count = 0
    for news in cursor:
        count += 1
        print(count)
        if 'class' not in news:
            print ('Populating classes...')
            title = news['title']
            topic = news_topic_modeling_service_client.classify(title)
            news['class'] = topic
            # upsert ==> if no document matches the filters, replace it with news
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)

            print('title is added!')