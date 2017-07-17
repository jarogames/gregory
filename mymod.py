#!/usr/bin/env python3
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


#########################################
#
#  PULL ZMQ - commands 
#
##########################################

def command_parser():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://127.0.0.1:5558")
    logger.info('socket 5558 open')
    collecter_data = {}
    x=0
    while True:
        x=x+1
        #logger.info('waiting to receive')
        result = receiver.recv_json()
        #result = receiver.recv(flags=zmq.NOBLOCK)# why not work?
        #logger.info('out of receive')
        if  result['client'] in collecter_data:
            collecter_data[result['client']] = collecter_data[result['client']] + 1
            logger.info('received {:d} {}'.format(result['client'],result['cmd']) )
        else:
            if result['cmd']=='register':
                collecter_data[result['client']] = 1
                logger.warning('NEW client {} registered {}'.format(result['client'],result['cmd']) )
            else:
                logger.error('NEW client {} MUST register - not {}'.format(result['client'],result['cmd']) )

        if x%10 == 0:
            pprint.pprint(collecter_data)
            time.sleep(1)
                
################################### CODE #############
#
#      CODE 
#
#######################################################
logge0.info('====== START argument=%s ====',args.book)  # start LOG file
command_parser()
#logge0.info('logging into %s',logfile)  # not actually important
logger.debug("hello")
logger.info("info")
logger.warn("warn")
logger.error("error")
logger.infoP("info plus")
logger.infoE("info exclam")

