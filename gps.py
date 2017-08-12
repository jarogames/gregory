#!/usr/bin/env python3
'''
based on mymod
one thread-   gps poll
next          keypress
check with gpsmon
- nex  staticmap
#pip3 install --user git+git://github.com/komoot/staticmap@master --upgrade #
TO INSTALL TILES
use foxtrotgps ; local server webmap..py and /tmp storage
OR
# downloadosmtiles --baseurl=http://localhost:8900 --lat=43:46.1  --lon=8.48:12.7 --zoom=12


'''
import mymod  
# .py is appended automatically

mymod.argparse_ini()
mymod.argparse_fin()
mymod.logging_ini()
mymod.logging_fin()
from mymod import logger,logger_head


import os
import subprocess
import time
#import threading
import threading
#####import context
import zmq
import tkinter_loop

#from mymod import logge0,args,command_parser_init,command_parser_step
from mymod import command_parser_init,command_parser_step

## From gps_socket (my) global variable should be loaded.
from gps_socket import translate_gps_line, gps_info

import keypress 
#################################
# procedures for threading:
#################################
def gps_poll():
    context =  zmq.Context.instance()
    receiver = context.socket(zmq.PAIR)
    receiver.connect("inproc://gps_poll")
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    logger.info("in     gps_poll thread")
    while (1==1):
        #time.sleep(0.1)
        translate_gps_line()
        event = poller.poll(100)
        if event:
            string=receiver.recv()
        else:
            string=""
        #logger.info(string)
        if string==b'q' or string==b'quit':break
    logger.error("OUT of gps_poll thread")
    return


def kpress_poll():
    context =  zmq.Context.instance()
    # receive from master
    receiver = context.socket(zmq.PAIR)
    receiver.connect("inproc://kpress_poll")
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    #string = receiver.recv()
    logger.info("in     kpress_poll thread ")
    #### THE BIG LOOP================
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect("tcp://127.0.0.1:5558")
    regs=0
    while (1==1):
        #time.sleep(0.1)
        # problem here... this stays HANGING
        keypress.producer_onestep(zmq_socket,True,True,regs)
        regs=1
        event = poller.poll(100)
        if event:
            string=receiver.recv()
        else:
            string=""
        #if not string is None and string!="":logger.info(string)
        if string==b'q' or string==b'quit':break
    logger.error("OUT of kpress_poll thread")
    return

########################
#   TK INTER LOOP - is blocking...
def tkinter_poll():
    
    context =  zmq.Context.instance()
    receiver = context.socket(zmq.PAIR)
    receiver.connect("inproc://tkinter_poll")
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    logger.info("in     tkinter_poll thread")
    die=False
    try:
        import tkinter
    except:
        logger.error("cannot import tkinter")
        die=True
    #if die:break
    # thi will also register input and 
    tkinter_loop.tk_init()  # tk_root.mainloop()
    tkinter_loop.tk_root.mainloop()
    #tkinter_loop.tk_root.quit()
    # while (1==1):
    #     #-----------------------
    #     #translate_gps_line()
    #     if not die:print(".",end="")
    #     #if not die:
    #     event = poller.poll(100)
    #     if event:
    #         string=receiver.recv()
    #     else:
    #         string=""
    #     #logger.info(string)
    #     if string==b'q':break
    logger.error("OUT of tkinter_poll thread ... wait 0.5s")
    time.sleep(0.5)
    return
#################################
#
#  MAIN
#
#################################
if __name__ == "__main__":
    # Prepare our context and sockets
    context = zmq.Context.instance()
    s_gps = context.socket(zmq.PAIR)
    s_gps.bind("inproc://gps_poll")
    context2 = zmq.Context.instance()
    s_key = context2.socket(zmq.PAIR)
    s_key.bind("inproc://kpress_poll")
    context3 = zmq.Context.instance()
    s_tki = context2.socket(zmq.PAIR)
    s_tki.bind("inproc://tkinter_poll")
    ############################## what should be initialized
    #                            # DO NOW:
    ### 1st thread - i would love to poll USB and fill GPS
    #   global variable
    t_gps_poll = threading.Thread(target=gps_poll)
    t_gps_poll.start()
    keypress.consumer_id=0
    t_keypress = threading.Thread(target=kpress_poll)
    t_keypress.start()
    t_tkinter = threading.Thread(target=tkinter_poll)
    t_tkinter.start()
    ################## - init command parser
    poller,receiver,collecter_data=command_parser_init()
    x=0
    ######### here all commands will pass in an infinite loop 
    while 1==1:
        # STATUS LINE HERE
        if gps_info['fix']=='+' and gps_info['dist']>0.:
            print(' '+gps_info['fix']+gps_info['timex']+
              " ({:6.4f},{:6.4f}){:6.1f} km/h {:6.1f} m H{:03.0f}  {:.1f}        ".format( gps_info['XCoor'],gps_info['YCoor'],gps_info['speed']*1.852,gps_info['altitude'],gps_info['course'],  gps_info['dist']*1000  ) ,end='\r')
            #here-  some distance was made from the last call
        else:
            print( "{} ".format(gps_info['fix']) , end="\r")


        #logger.info("entering parser") # wait 100ms fin c.p.step
        cmd=command_parser_step(poller,receiver,collecter_data,x)
        if len(cmd)>0:print(">",cmd)
        if cmd!="":
            s_gps.send_string(cmd)
            s_key.send_string(cmd)
            s_tki.send_string(cmd) # but it is blocking
            tkinter_loop.tk_command=cmd
        if cmd=="q" or cmd=="quit": break
        x=x+1
    #t_gps_poll.exit()
    #t_keypress.exit()
