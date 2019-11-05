# -*- coding: utf-8 -*-
from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://fqamwhqy:BQzksKwYVc7iwsl6cxL99VEAhFW5sWiY@beaver.rmq.cloudamqp.com/fqamwhqy"

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test passed!'

if __name__ == "__main__":
    test_basic()


