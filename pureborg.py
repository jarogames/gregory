#!/usr/bin/env python3

############################################
#  python interface to a regular BORG backup
############################################
#FROM=$HOME/MZ_TATICEK/GoogleDriveJaromrax/
#TO=$HOME/Dropbox/__old_files_unsorted_jarom/GoogleDriveJaromrax/
#
#cd $FROM
#grive -f   # always download not upload
#echo "======== SYNCING FROM GOOGLEDRIVE TO ~/Dropbox ....  "
#rsync -av --progress $FROM $TO

# ===================from borg:
#!/bin/sh
# REPOSITORY=username@remoteserver.com:backup

# # Setting this, so you won't be asked for your repository passphrase:
# export BORG_PASSPHRASE='XYZl0ngandsecurepa_55_phrasea&&123'
# # or this to ask an external program to supply the passphrase:
# export BORG_PASSCOMMAND='pass show backup'

# # Backup all of /home and /var/www except a few
# # excluded directories
# borg create -v --stats                          \
#     $REPOSITORY::'{hostname}-{now:%Y-%m-%d}'    \
#     /home                                       \
#     /var/www                                    \
#     --exclude '/home/*/.cache'                  \
#     --exclude /home/Ben/Music/Justin\ Bieber    \
#     --exclude '*.pyc'

# # Use the `prune` subcommand to maintain 7 daily, 4 weekly and 6 monthly
# # archives of THIS machine. The '{hostname}-' prefix is very important to
# # limit prune's operation to this machine's archives and not apply to
# # other machine's archives also.
# borg prune -v --list $REPOSITORY --prefix '{hostname}-' \
#     --keep-daily=7 --keep-weekly=4 --keep-monthly=6

import mymod
mymod.argparse_ini()
mymod.argparse_fin()
mymod.logging_ini()
mymod.logging_fin()
from mymod import logger,logger_head

import os
import subprocess
import time
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

CONFIGFILE=os.environ['HOME']+"/.borgbackup_pairs"

def get_hostname():
    import socket
    return socket.gethostname()

def get_signature():
    import datetime
    r=get_hostname()
    r=r+"_"+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%a')
    return r


def prune_repo(repo):
    CMD='borg prune -v --list '
    CMD=CMD+repo
    CMD=CMD+' --prefix '+get_hostname()+' '
    CMD=CMD+' --keep-within=7d --keep-weekly=4 --keep-monthly=-1 '
    logger.infoC( CMD )
    return


def load_addr_repo_pairs():
    global logger
    logger.info("going to INIT")
    li=[]
    try:
        with open(CONFIGFILE) as f:
            li=f.readlines()
    except:
        logger.error("NO FILE "+CONFIGFILE+' / quit')
        quit()
    # clean lines
    li=[ i.strip() for i in li]
    # remove \n and comments
    li=[ i for i in li if len(i)>0 and i.strip()[0]!="#"]
    # divide into pairs
    li=[ i.split() for i in li]
    return li


def mail_out_results( SIG, ok, nok ):
    global results
    texth=SIG+" OK="+str(ok)+" BAD="+str(nok)
    logger.infoP("mailing results: OK="+str(ok)+" BAD="+str(nok) )
   
    # Create a text/plain message
    #    msg = MIMEText(fp.read())
    textb=""
    for i in results:
        textb=textb+"  ".join(i)+"\n"
    msg=MIMEText( textb )
    me="borg@localhost"# == the sender's email address
    you="root@localhost"# you == the recipient's email address
    msg['Subject'] = 'BORG '+texth
    msg['From'] = me
    msg['To'] = you
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    return


def unmount_sshfs(dest):
    CMD="fusermount -u "+dest
    logger.infoC( CMD )
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        logger.infoP("ok")
        logger.infoP(res)
    except subprocess.CalledProcessError as grepexc:
        logger.error("error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        logger.error("cannot unmount "+dest)
        countdown("problem",10)
        quit()
    
def mount_sshfs( server_folder):
    MODIR="~/BORGBACKUP/mount_sshfs/"
    MODIR=os.path.expanduser(MODIR)
    if not os.path.isdir(MODIR):
        logger.error("I need to have "+MODIR+" to backup")
        quit()
    CMD="sshfs "+server_folder+" "+MODIR
    logger.infoC( CMD )
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        logger.infoP("ok")
        logger.infoP(res)
    except subprocess.CalledProcessError as grepexc:
        logger.error("error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        logger.error("cannot init NEW borg REPO") # MOSTLY already EXist
        countdown("problem",10)
        return ""
        #quit()# no quit possible inside
    return MODIR
    
def borg_init( repo ):
    '''
    first is borg init /path/to/repo
    '''
    CMD="borg init --encryption=none "+repo
    logger.infoC( CMD )
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        logger.infoP("ok")
        logger.infoP(res)
    except subprocess.CalledProcessError as grepexc:
        logger.error("error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        logger.error("cannot init NEW borg REPO")
        countdown("problem",10)
    return


def borg_create( repo , sig, directory ):
    '''
    borg create /path/to/repo::Monday ~/src ~/Documents 
    borg create -v --stats /path/to/repo::Tuesday ~/src ~/Documents
    '''
    ssh=False
    # if directory  is ssh address:   ~ must be expanded
    if not os.path.isdir( os.path.expanduser(directory) ):
        logger.warning("directory "+directory+" doesnt exist")
        host=directory.split(":")[0]
        CMD="ping "+host+" -w 1"
        logger.infoC( CMD)
        try:
            reslist=subprocess.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
            logger.infoP("ok - host "+host+" lives")
            ssh=True
            # newly the DIR will be mounted 
            directory=mount_sshfs(directory)
            if directory=="": return "??"
        except subprocess.CalledProcessError as grepexc:
            logger.error("error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
            logger.error("no host - no directory")
            return "??"

    OPTIONS=" -v --stats --compression lzma,9 --info "
    CMD="borg create "+OPTIONS+" "+repo+"::"+sig+" "+directory
    logger.infoC( CMD )
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        logger.infoP("ok")
        logger.infoP(res)
    except subprocess.CalledProcessError as grepexc:
        logger.error("error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        #quit() # if problem, i dont want to QUIT before others
        logger.error("cannot create backup")
        if ssh:unmount_sshfs(directory)
        countdown("problem",10)
        return "xx"
    #logger.info( CMD )
    if ssh:unmount_sshfs(directory)
    return "ok"


def borg_info( repo, stamp):
    CMD="borg info "+repo+"::"+stamp
    logger.infoC( CMD)
    res2=subprocess.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    #logger.infoP(res2[1])  #  finger; 2 host; 3 user;
    #logger.infoP(res2[4])  # 
    logger.infoP(res2[5])  # time end
    logger.infoP(res2[6].split()[-1])  # cmdline; directory
    logger.infoP(res2[7])  # num fiules
    #logger.infoP(res2[8]) # space
    logger.infoP(res2[9])
    logger.infoP(res2[10])
    logger.infoP(res2[11])
    #logger.infoP(res2[12]) # space 
    return


def borg_list( repo ):
    '''
    I use `borg list repo`
    and `borg info repo::last_stamp`   
    '''
    CMD="borg list  "+repo
    logger.infoC( CMD)
    try:
        reslist=subprocess.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
        logger.infoP("ok"+str(len(reslist)))
    except subprocess.CalledProcessError as grepexc:
        logger.error("error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        return ""
    if not reslist[-1].rstrip()=="": 
        res=reslist[-1].split()[0]
    else:
        return ""
    logger.infoP( res )
    borg_info( repo, res )
    return res


def countdown(txt, n):
    vin="|"
    out="|"
    for i in range(n):
        print(txt,vin+"."*(n-1)+ out+" ", i+1,"/",n, end="\r")
        print(txt,vin+"="*(i)+">"+"."*(n-i-1)+out , end="\r")
        time.sleep(1)
    #quit()

#################################
#
#  MAIN
#
#################################
SIGNATURE=get_signature()
logger.info( SIGNATURE )
pairs=load_addr_repo_pairs()
results=[]
ok=0
nok=0
for li in pairs:
    logger_head.infoX( li[1] )
    logger.info( li[0]+" - "+li[1] )
    last=borg_list( li[0] )
    if last=="":
        countdown("initialize new repository?",15)
        borg_init( li[0] )
    if last=="X":
        countdown("Unknown directory os host",15)
        continue
    logger_head.infoC(last+" ==> "+SIGNATURE)
    countdown("create new backup?",8)
    res=borg_create( li[0], SIGNATURE , li[1] )
    results.append( [res,li[1]]  )
    print( results )
    if res=="ok":
        borg_info(li[0], SIGNATURE)
        ok=ok+1
    else:
        nok=nok+1
mail_out_results(SIGNATURE, ok, nok )
print( results )

