#!/usr/bin/env python3
############################################
#  python interface to a regular BORG backup
#
#
####################################
#  PYTHON TEPLATE 
# ===================
# (all programs should be based on)
#  logging; argsparse threads; zmq messages
#####################################
#pip3 install --user git+https://github.com/metachris/logzero 
####################################### args
import argparse
###
import logging
from logzero import setup_logger,LogFormatter
###  to get prgname
import os, sys
###  to wait in RECV queue
import time
import zmq
import pprint # print json line

######################################### arguments parser ####
parser=argparse.ArgumentParser(description="""
 ... 
 ...
""")

parser.add_argument('book', default="", help='')
parser.add_argument('-d','--debug', action="store_true", help='debug level log')#,required=True
args=parser.parse_args()
print('Main argument=',args.book)

####################################### logging, logzero ######

logging.addLevelName(19, "+PLUS")
def infoP(self, message, *args, **kws):
    if self.isEnabledFor(19):self._log(19, message, args, **kws) 
logging.Logger.infoP = infoP
logging.addLevelName(18, "!PROBLEM")
def infoE(self, message, *args, **kws):
    if self.isEnabledFor(18):self._log(18, message, args, **kws) 
logging.Logger.infoE = infoE

log_forma0 = '%(color)s%(levelname)1.1s%(levelno)s.  %(asctime)s %(module)s:%(lineno)d%(end_color)s %(message)s'
log_format = '%(color)s%(levelname)1.1s... %(end_color)s %(message)s'  # i...  format
formatte0 = LogFormatter(fmt=log_forma0,datefmt='%Y-%m-%d %H:%M:%S')
formatter = LogFormatter(fmt=log_format)
loglevel=1 if args.debug==1 else 11  # all info, but not debug
logfile=os.path.splitext(os.path.basename(sys.argv[0]) )[0]+'.log'
logge0 = setup_logger( name="head",logfile=logfile, level=loglevel,formatter=formatte0 )#to 1-50
logger = setup_logger( name="main",logfile=logfile, level=loglevel,formatter=formatter )#to 1-50

#######################################  input: cmdline/keypress/programs #####
def command_parser():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    ##   #receiver.RCVTIMEO = 1000 ### in zmq 3.0 #receiver.LINGER=0  ##
    receiver.bind("tcp://127.0.0.1:5558")
    logger.info('ZMQ PULL socket on 5558 is open')
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN) # POLLIN for recv, POLLOUT for send
    collecter_data = {}
    x=0
    while True:
        x=x+1
        #logger.info('waiting to receive')
        #result = receiver.recv_json()
        event=poller.poll(100)  # wait 100ms
        if event:
            result = receiver.recv_json()
            logger.info('out of receive')
            if   result['consumer'] in collecter_data:
                collecter_data[result['consumer']] = collecter_data[result['consumer']] + 1
                logger.info('received {:d} {}'.format(result['consumer'],result['num']) )
            else:
                collecter_data[result['consumer']] = 1
                logger.warning('reset with {} {}'.format(result['consumer'],result['num']) )

            if x%10 == 0:
                pprint.pprint(collecter_data)
                time.sleep(1)
def command_parser_init():
    '''
    poller and receiver it is clear: 
    collecter_data  contains number of commands comming from a PUSH;1==new
    '''
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    ##   #receiver.RCVTIMEO = 1000 ### in zmq 3.0 #receiver.LINGER=0  ##
    receiver.bind("tcp://127.0.0.1:5558")
    logger.info('ZMQ PULL socket on 5558 is open')
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN) # POLLIN for recv, POLLOUT for send
    collecter_data = {}
    return poller,receiver,collecter_data
def command_parser_step(poller,receiver,collecter_data,x):
    event=poller.poll(100)  # wait 100ms
    if event:
        result = receiver.recv_json()
        logger.info('out of receive')
        if   result['consumer'] in collecter_data:
            collecter_data[result['consumer']] = collecter_data[result['consumer']] + 1
            logger.info('received {:d} {}'.format(result['consumer'],result['num']) )
        else:
            collecter_data[result['consumer']] = 1
            logger.warning('reset with {} {}'.format(result['consumer'],result['num']) )

        if x%10 == 0:
            pprint.pprint(collecter_data)
            time.sleep(1)
    return x+1

###########################################FUNCTIONS###
#
# 
#
######################################################
def mail_result():
    logger.infoP("mailing")
    return
def borg_create():
    logger.infoP("creating BORG")
    return
def borg_status():
    logger.infoP("geting   BORG status")
    return

################################### CODE #############
#
#      CODE 
#
#######################################################
logge0.info('====== START argument=%s ====',args.book)  # start LOG file
poller,receiver,collecter_data=command_parser_init()
x=0
while 1==1:
    #logger.info("entering parser")
    x=command_parser_step(poller,receiver,collecter_data,x)
    #command_parser()  # i would like to have None or INPUT
    #logger.info("out of  parser")
#logge0.info('logging into %s',logfile)  # not actually important
logger.debug("hello")
logger.info("info")
logger.warn("warn")
logger.error("error")
logger.infoP("info plus")
logger.infoE("info exclam")

