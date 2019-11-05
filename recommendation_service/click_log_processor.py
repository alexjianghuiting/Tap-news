# update the user's preference model
# Time decay model:
# If selected:
# p = (1-α)p + α
# If not:
# p = (1-α)p
# p = selection probability = INITIAL_P = 1.0 / NUM_OF_CLASSES

import news_classes
import os
import sys

import common.mongodb_client as mongodb_client
import common.cloudAMQP_client as CloudAMQPClient

NUM_OF_CLASSES = 17
INITIAL_P = 1 / NUM_OF_CLASSES # 就算不是1.0除以也是小数
ALPHA = 0.1

SLEEP_TIME_IN_SECONDS = 1
LOG_CLICKS_TASK_QUEUE_URL = "amqp://vgscksqh:H9iWraK8W1Rh9-sqKS-YpT-fHztO3lZY@otter.rmq.cloudamqp.com/vgscksqh"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-log-task-queue"

PREFERENCE_MODEL_NAME = "user_preference_model"
NEWS_NAME = "news"

cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return

    if ('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']

    # update user preference
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_NAME].find_one({'userId':userId})

    if model is None:
        print("Creating preference model for new user: %s" % userId)
        new_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)

        new_model['preference'] = preference
        model = new_model

    print("Updating preference model for new user: %s" % userId)

    # most recent one
    news = db[NEWS_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in news_classes.classes):
        print('Skipping processing...')
        return

    click_class = news['class']
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    # 其它所有没click的items
    for i, prob in model['preference'].iteritems():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'])

    # 改了model['preference']之后 把整个model传进去
    db[PREFERENCE_MODEL_NAME].replace_one({'userId': userId}, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
                cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()