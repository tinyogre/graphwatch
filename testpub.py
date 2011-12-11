import zmq
import os
import simplejson as json
import time

ctx = zmq.Context()
socket = ctx.socket(zmq.PUB)
socket.bind('tcp://*:11100')
next_node = 1

while True:
    msg = {'newNode': {'name': 'node' + str(next_node) }}
    socket.send(json.dumps(msg))
    msg = {'newEdge': {'from': 'node' + str(next_node - 1), 
                       'to': 'node' + str(next_node)}}
    socket.send(json.dumps(msg))
    time.sleep(1)
    next_node += 1
