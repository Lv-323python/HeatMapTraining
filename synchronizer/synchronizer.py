# 1) set start time 01.00
#
#
# import:
import json
from general_helper.postgres_helpers.user_request import get_all_requests
from general_helper.mongodb_helpers.mongodb_request_sender import MongoDBRequestSender
from general_helper.rabbitmq_helpers.request_sender_client import RequestSenderClient
from general_helper.rabbitmq_helpers.request_sender_client_config import HOST, PORT
# 1)Postgres
# 2)MongoDB
# 3)Rabbit, producer(client) part
# 4)
#
#
#
#
# 1. get all users id, make list
#
# 2. get all requests with get_commits, make list.
# with scoped_session() as session:
#         return session.query(UserRequests).filter_by(user_id=user_id)
#
# 3.1. get user get_commits response from MongoDB
# 3.2. get updated response
# 3.3. delete old response from MongoDB
# 3.4. set updated response to MongoDB
#
#
#

def update_commits(user_request):
    # get old commits
    mongo_request_sender = MongoDBRequestSender()
    message = user_request
    message['action'] = 'get_updated_all_commits'
    message['old_commits'] = mongo_request_sender.get_entry(user_request)

    # get 'user get_commits response' from MongoDB
    request_sender_rpc = RequestSenderClient(host=HOST, port=PORT)
    new_response = request_sender_rpc.call(json.dumps(message))

    # delete old response from MongoDB
    mongo_request_sender.delete_entry(user_request)

    # set updated response to MongoDB
    mongo_request_sender.set_entry(user_request, new_response)

    return new_response


