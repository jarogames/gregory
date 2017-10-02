#!/usr/bin/env python3
#################################### 1
#  PYTHON TEPLATE 
# ===================
# (all programs should be based on)
#  logging; argsparse threads; zmq messages
#####################################
#pip3 install --upgrade  git+https://github.com/metachris/logzero 
#pip3 install --user git+https://github.com/metachris/logzero 
####################################### args
import argparse
###
import logging
from logzero import setup_logger,LogFormatter,colors
###  to get prgname
import os, sys
###  to wait in RECV queue
import time
import zmq
import pprint # print json line
print("... I am in mymod.py ................")
######################################### arguments parser ####
parser=None
args=None
def argparse_ini(description="..."):
    global parser,args
    parser=argparse.ArgumentParser(description=description)
   
#parser.add_argument('book', default="", help='')  # obligatory arg.

def argparse_fin():
    global parser,args
    parser.add_argument('--debug', action="store_true", help='debug level log')#,required=True
    args=parser.parse_args()
    #print('Main argument=',args.book)

####################################### logging, logzero ######
logger=None
logger_head=None
def logging_ini():
    global logging,logger,logger_head
    logging.addLevelName(19, "+PLUS")
    def infoP(self, message, *args, **kws):
        if self.isEnabledFor(19):self._log(19, message, args, **kws) 
    logging.Logger.infoP = infoP
    LogFormatter.DEFAULT_COLORS[19] = colors.Fore.CYAN
    
    logging.addLevelName(18, "!PROBLEM")
    def infoE(self, message, *args, **kws):
        if self.isEnabledFor(18):self._log(18, message, args, **kws) 
    logging.Logger.infoE = infoE
    LogFormatter.DEFAULT_COLORS[18] = colors.Fore.RED

    logging.addLevelName(17, "xBADTHING")
    def infoX(self, message, *args, **kws):
        if self.isEnabledFor(17):self._log(17, message, args, **kws) 
    logging.Logger.infoX = infoX
    LogFormatter.DEFAULT_COLORS[17] = colors.Fore.CYAN

    logging.addLevelName(16, "cCOMMAND")
    def infoC(self, message, *args, **kws):
        if self.isEnabledFor(16):self._log(16, message, args, **kws) 
    logging.Logger.infoC = infoC
    LogFormatter.DEFAULT_COLORS[16] = colors.Fore.YELLOW

    log_forma0 = '%(color)s%(levelname)1.1s%(levelno)s.  %(asctime)s %(module)s:%(lineno)d%(end_color)s %(message)s'
    log_forma0 = '%(color)s%(asctime)s %(message)s%(end_color)s'
    log_format = '%(color)s%(levelname)1.1s... %(end_color)s %(message)s'  # i...  format
    formatte0 = LogFormatter(fmt=log_forma0,datefmt='%Y-%m-%d %H:%M:%S')
    formatter = LogFormatter(fmt=log_format)
    loglevel=1 if args.debug==1 else 11  # all info, but not debug
    logfile=os.path.splitext(os.path.basename(sys.argv[0]) )[0]+'.log'
    logger_head = setup_logger( name="head",logfile=logfile, level=loglevel,formatter=formatte0 )#to 1-50
    logger = setup_logger( name="main",logfile=logfile, level=loglevel,formatter=formatter )#to 1-50

def logging_fin():
    global logging,logger,logger_head
    logger_head.info("======================================================")
    logger_head.info("====== START /%s ====",args)
    logger.info("ok")
    return
        
#######################################  input: cmdline/keypress/programs #####
#########################################
#
#  PULL ZMQ - commands 
#
##########################################
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
    result={}
    result['cmd']=""
    if event:
        result = receiver.recv_json()
        #logger.info('out of receive')
        if  result['client'] in collecter_data:
            collecter_data[result['client']] = collecter_data[result['client']] + 1
            if result['cmd']!="":
                logger.info('from {:d}: {}'.format(result['client'],result['cmd']) )
        else:
            if result['cmd']=='register':
                collecter_data[result['client']] = 1
                logger.warning('NEW client {} registered {}'.format(result['client'],result['cmd']) )
                return ""
                            
            else:
                logger.error('NEW client {} MUST register - not {}'.format(result['client'],result['cmd']) )
                return ""

        #if x%100 == 0:   pprint.pprint(collecter_data)
    return result['cmd']

###########################################FUNCTIONS###
#
# 
#
######################################################

################################### CODE #############
#
#      CODE 
#
#######################################################
if __name__ == "__main__":
 
    argparse_ini()
    argparse_fin()
    logging_ini()
    logging_fin()
    
    #- init command parser
    poller,receiver,collecter_data=command_parser_init()
    x=0
    while 1==1:
        #logger.info("entering parser")
        cmd=command_parser_step(poller,receiver,collecter_data,x)
        if len(cmd)>0:print(">",cmd)
        if cmd=="q": break
        x=x+1
        #- end command parser loop    
    #logger_head.info('logging into %s',logfile)  # not actually important
    logger.debug("hello")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")
    logger.infoP("info plus")
    logger.infoE("info exclam")

