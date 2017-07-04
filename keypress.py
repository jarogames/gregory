#!/usr/bin/env python3
import time
import zmq
import random
consumer_id = random.randrange(1,10005)

import termios, sys, os
TERMIOS = termios

def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 999)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c


def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    #zmq_socket.bind("tcp://127.0.0.1:5558")
    zmq_socket.connect("tcp://127.0.0.1:5558")
    # Start your result manager and workers before you start your producers
    for num in range(200):
        key=getkey()
        print('KEY=',key)

        if key==b' ':key=b'SPC'
        if key==b'\n':key=b'ENT'
        if key==b'\x7f':key=b'BKSP'
        if key==b'\x1b[3~':key=b'DEL'
        if key==b'\x1b[A':key=b'UP'
        if key==b'\x1b[B':key=b'DOWN'
        if key==b'\x1b[C':key=b'RIGHT'
        if key==b'\x1b[D':key=b'LEFT'
        if key==b'\x1b[H':key=b'HOME'
        if key==b'\x1b[F':key=b'END'
        if key==b'\x1b[5~':key=b'PGUP'
        if key==b'\x1b[6~':key=b'PGDN'
        if key==b'\x1b\x1b':key=b'ESCESC'
        key=key.decode('utf8')
        print('KEY=',key)
        ##print(key, end='' )
        work_message =  { 'consumer' : consumer_id, 'num' : key}
        #{ 'num' : num }
        zmq_socket.send_json(work_message)
        time.sleep(0.05)

producer()
