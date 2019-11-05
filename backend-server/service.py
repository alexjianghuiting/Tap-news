# -*- coding: utf-8 -*-
import pyjsonrpc
import os
import sys

# mongodb用的是bson
from bson.json_util import dumps

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    # 一个api 看文档
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add is called with %d and %d" % (a, b)
        return a + b

    @pyjsonrpc.rpcmethod
    def getNews(self):
        db = mongodb_client.get_db()
        news = list(db['news'].find())
        # iterable转化成list
        return json.loads(dumps(news))

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()