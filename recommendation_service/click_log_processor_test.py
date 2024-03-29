import os
import sys
from datetime import datetime
from sets import Set

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import common.mongodb_client as mongodb_client
import recommendation_service.click_log_processor as click_log_processor

PREFERENCE_MODEL_NAME = "user_preference_model"
NEWS_NAME = "news"

NUM_CLASSES = 17

def test_basic():
    db = mongodb_client.get_db()
    db[PREFERENCE_MODEL_NAME].delete_many({"userId": "test_user"})

    msg = {"userId": "test_user",
           "newsId": "test_news",
           "timestamp": str(datetime.utcnow())}

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_NAME].find_one({'userId':'test_user'})
    assert model is not None
    assert len(model['preference']) == NUM_CLASSES

    print('test_basic passed!')

if __name__ == '__main__':
    test_basic()