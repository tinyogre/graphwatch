#!/usr/bin/env python
from os import path as op
import os

import tornado.web
import tornadio
import tornadio.router
import tornadio.server
import simplejson
import tornado.ioloop
ioloop = tornado.ioloop.IOLoop.instance()

ROOT = op.normpath(op.dirname(__file__))
next_id = 1
next_node = 1

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the front page"""
    def get(self):
        self.render("static/index.html")

class Server:
    clients = set()

    def __init__(self):
        pass

    def send(self, client, packet):
        client.send(packet)

    def broadcast(self, packet):
        print 'broadcast: ' + simplejson.dumps(packet)
        for c in self.clients:
            c.send(packet)

server = Server()

class Client(tornadio.SocketConnection):
    def on_open(self, *args, **kwargs):
        global next_id
        server.clients.add(self)
        self.id = next_id;
        print 'Created client ' + str(self.id)
        next_id += 1;
        packet = {'init': {'id': self.id}}
        server.send(self, packet)
        
    def on_message(self, message):
        pass

    def on_close(self):
        server.clients.remove(self)
        packet = {'left': {'id': self.id}}
        server.broadcast(packet)
        
settings = {
    'static_path': op.join(op.dirname(__file__), 'static'),
}

#use the routes classmethod to build the correct resource
Router = tornadio.get_router(Client)

#configure the Tornado application
application = tornado.web.Application(
    [(r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])), 
     (r"/", IndexHandler), 
     Router.route()],
    enabled_protocols = ['websocket',
                         'flashsocket',
                         'xhr-multipart',
                         'xhr-polling'],
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 11001
)

def idle():
    print 'idle'
    global next_node
    msg = {'newNode': {'name': 'node' + str(next_node) }}
    server.broadcast(msg)
    msg = {'newEdge': {'from': 'node' + str(next_node - 1), 
                       'to': 'node' + str(next_node)}}
    server.broadcast(msg)
    next_node += 1

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(idle, 1000).start()

    tornadio.server.SocketServer(application, io_loop=io_loop)


