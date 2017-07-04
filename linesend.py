#!/usr/bin/env python3
import time
import zmq
import random
consumer_id = random.randrange(1,10005)

import  sys, os

def getline():
    c = None
    print("Enter/Paste your content. Ctrl-D to save it.")
    line=''
    line = input("")
    return line


def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    #zmq_socket.bind("tcp://127.0.0.1:5558")
    zmq_socket.connect("tcp://127.0.0.1:5558")
    # Start your result manager and workers before you start your producers
    for num in range(200):
        line=getline()
        work_message =  { 'consumer' : consumer_id, 'num' : line}
        #{ 'num' : num }
        zmq_socket.send_json(work_message)
        time.sleep(0.05)
producer()
