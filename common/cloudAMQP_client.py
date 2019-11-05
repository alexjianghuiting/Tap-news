# -*- coding: utf-8 -*-
import pika
import json
# pika用法
# 定义一个class
class CloudAMQPClient:
    # 连到queue上 要能使用不同的queue 自己用 自己开一个instance 自己关了 不会影响别人
    # queue_declare() queue已经存在了 不会duplicate创建
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

       # send a message
    def sendMessage(self, message):
       self.channel.basic_publish(exchange='',
                                  routing_key=self.queue_name,
                                  body=json.dumps(message))
       print "[X] sent message to %s: %s" % (self.queue_name, message)

       # get a message
       # 有method_frame = 有消息
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            print "[0] Received message from %s: %s" % (self.queue_name, body)
            # 要发送basic_ack acknowledgement 如果不发 这个信息就不会被删掉 就会被重复接收 就会导致dupilicate
            # 要有个delivery_tag
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print "No message returned"
            return None
   # 爬虫 ip会被block
   # 如果让python整个sleep cloudAMQP整个就断了 就算没有通信 client也要和远程服务器通信 heartbeat 每十秒钟
   # 保证sleep且连接不断
    def sleep(self, seconds):
       self.connection.sleep(seconds)

