#!/usr/bin/env python3
import time
import zmq
import random

consumer_id=-1
#consumer_id = random.randrange(1,100050)

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


def producer_onestep(zmq_socket,register=False,silent=False,regs=0):
    key=getkey()
    if regs==0 and register:
        print("...registering......")
        key1='register'
        work_message =  { 'client' : consumer_id, 'cmd' : key1}
        zmq_socket.send_json(work_message)
        regs=1

    ###if not silent:print('KEY=',key)
    if not register:
        if key==b'r':key=b'r'
    else:
        if key==b'r':key=b'register'

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
    if not silent:print('KEY=',key)
    ##print(key, end='' )
    work_message =  { 'client' : consumer_id, 'cmd' : key}
    #{ 'num' : num }
    zmq_socket.send_json(work_message)
    time.sleep(0.05)
    
def producer(register=False,silent=False):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    #zmq_socket.bind("tcp://127.0.0.1:5558")
    zmq_socket.connect("tcp://127.0.0.1:5558")
    # Start your result manager and workers before you start your producers
    regs=0
    for num in range(123456789):
        ####one_step
        ### regs++
        key=getkey()
        if regs==0 and register:
            print("...registering......")
            key1='register'
            work_message =  { 'client' : consumer_id, 'cmd' : key1}
            zmq_socket.send_json(work_message)
            regs=1

        ###if not silent:print('KEY=',key)
        if register:
            if key==b'r':key=b'r'
        else:
            if key==b'r':key=b'register'

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
        if not silent:print('KEY=',key)
        ##print(key, end='' )
        work_message =  { 'client' : consumer_id, 'cmd' : key}
        #{ 'num' : num }
        zmq_socket.send_json(work_message)
        time.sleep(0.05)

if __name__ == "__main__":
    consumer_id = random.randrange(1,100050)
    producer()
