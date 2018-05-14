import gevent
from .. import app
from .. import redis
from .. import sockets
from . import websocket
import ast
from handler import *

REDIS_URL = "redis://localhost:6379/0"
REDIS_CHAN = 'auction'

class SocketBroker():

    @sockets.route('/submit')
    def inbox(ws):
        while not ws.closed:
            # Sleep to prevent *constant* context-switches.
            gevent.sleep(0.1)
            message = ws.receive()
            data = ast.literal_eval(message)
            message = offer_bid(data)

            if message:
                app.logger.info(u'Inserting message: {}'.format(message))
                redis.publish(REDIS_CHAN, message)

    @sockets.route('/receive')
    def outbox(ws):
        websocket.register(ws)
        while not ws.closed:
            # Context switch while `ChatBackend.start` is running in the background.
            gevent.sleep(0.1)

broker = SocketBroker()
