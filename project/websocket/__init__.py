# import gevent
# from .. import app
# from .. import redis
# from flask_restful import Resource

# REDIS_URL = "redis://localhost:6379/0"
# REDIS_CHAN = 'auction'




# class SocketBackend(object):
#     """Interface for registering and updating WebSocket clients."""

#     def __init__(self):
#         self.clients = list()
#         self.pubsub = redis.pubsub()
#         self.pubsub.subscribe(REDIS_CHAN)

#     def __iter_data(self):
#         for message in self.pubsub.listen():
#             data = message.get('data')
#             if message['type'] == 'message':
#                 app.logger.info('Sending message: {}'.format(data))
#                 yield data

#     def register(self, client):
#         """Register a WebSocket connection for Redis updates."""
#         self.clients.append(client)

#     def send(self, client, data):
#         """Send given data to the registered client.
#         Automatically discards invalid connections."""
#         try:
#             client.send(data)
#         except Exception:
#             self.clients.remove(client)

#     def run(self):
#         """Listens for new messages in Redis, and sends them to clients."""
#         for data in self.__iter_data():
#             for client in self.clients:
#                 gevent.spawn(self.send, client, data)

#     def start(self):
#         """Maintains Redis subscription in the background."""
#         gevent.spawn(self.run)

# websocket = SocketBackend()
# websocket.start()
