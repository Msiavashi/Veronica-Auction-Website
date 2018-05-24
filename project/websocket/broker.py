import gevent
from .. import app
from .. import redis
# from .. import sockets
from . import websocket
import ast
from handler import *
from project import socketio
from flask import session
from flask_socketio import join_room, leave_room, emit
REDIS_URL = "redis://localhost:6379/0"
REDIS_CHAN = 'auction'



# @socketio.on('submit', '/submit')
# def inbox(json):
#     while not ws.closed:
#         # Sleep to prevent *constant* context-switches.
#         gevent.sleep(0.1)
#         message = ws.receive()
#         data = ast.literal_eval(message)
#         handler = data['handler']
#         if handler == 'offer':
#             message = offer_bid(data)
#         elif handler == 'loadview':
#             message = loadview(data)
#         elif handler == 'auction_done':
#             message = auction_done(data)
#         else:
#             pass

#         if message:
#             app.logger.info(u'Inserting message: {}'.format(message))
#             redis.publish(REDIS_CHAN, message)

# @sockets.route('/receive')
# def outbox(ws):
#     websocket.register(ws)
#     while not ws.closed:
#         # Context switch while `ChatBackend.start` is running in the background.
#         gevent.sleep(0.1)

