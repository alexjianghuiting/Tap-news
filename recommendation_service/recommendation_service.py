import operator
import os
import sys

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import common.mongodb_client as mongodb_client

PREFERENCE_MODEL_NAME = "user_preference_model"
SERVER_HOST = 'localhost'
SERVER_PORT = 5050

# Ref: http://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getPreferenceForUser(user_id):
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_NAME].find_one({'userId':user_id})
    if model is None:
        return []

    sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]

    # returns [] if the first one is the same as the last one
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []

    return sorted_list

# Threading HTTP Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')

print("Starting RPC-recommendation server on %s:%d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()