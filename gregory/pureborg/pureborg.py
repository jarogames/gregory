#!/usr/bin/env python3
#
#  /etc/fstab ========================= FOR USB :
# UUID=9E70-9058  /media/ojr/9E70-9058  auto rw,user,exec,umask=000,nofail  0 3
# UUID=9E70-9058  /media/ojr/9E70-9058  auto rw,user,exec,umask=000,nofail  0 3
# ======== new thing - i want owncloud here but not mounted, mountable on demand
# https://owncloud.cesnet.cz/remote.php/webdav/ 	/mnt/owncloud 	davfs 	rw,noauto,user	0		0
#
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

### THIS=argpar+loggin MUST BE HERE???? ##############
### original import mymod worked locally only
from gregory.mymod import mymod   # this is ok with gregory install
mymod.argparse_ini()
mymod.parser.add_argument('--list', '-l',action="store_true", help='list')
mymod.parser.add_argument('--mount', '-m',action="store_true", help='borg mount with zenity')
mymod.argparse_fin()
mymod.logging_ini()
mymod.logging_fin()
###from mymod import logger,logger_head # worked localy
from gregory.mymod.mymod import logger,logger_head

import os
import subprocess
import time
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

import glob  # i want to parse ~/.*  config

#CONFIGFILE=os.environ['HOME']+"/.borgbackup_pairs"
CONFIGFILE=os.environ['HOME']+"/.pureborg.pairs"


######## FROM A TEST WITH ZENITY #######  MOUNT THE BACKUP
from zenipy import calendar,message,error,warning,question,entry,password,file_selection,scale,color_selection,zlist

MOUNTPOINT=os.path.expanduser("~/BORGBACKUP/recovery_mount_point")
if not os.path.isdir( MOUNTPOINT ):
    print("!... creating",MOUNTPOINT)
    os.makedirs(MOUNTPOINT)


#-------------- borg mount / fusermount -u ----
def UMOUNT():    
    CMD="fusermount -u "+MOUNTPOINT
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        print("i... ok"+res)
    except subprocess.CalledProcessError as grepexc:
        print("e... mount:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))

def MOUNT(mou):        
    CMD="fusermount "+mou+" "+MOUNTPOINT
    CMD="borg mount "+mou+" "+MOUNTPOINT
    print("i...",CMD)
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        print("i... ok"+res)
    except subprocess.CalledProcessError as grepexc:
        print("e... mount:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))

def RUNXTERM():
    CMD="xterm -fa 'Monospace' -fs 14 -e 'cd ~/BORGBACKUP/recovery_mount_point;mc' "
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        print("i... ok"+res)
    except subprocess.CalledProcessError as grepexc:
        print("e... mount:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))

def MOUNTUMOUNT():
 
    with open(CONFIGFILE) as f:
        lines=f.readlines()
    lines=[ x.rstrip() for x in lines if x[0]!="#"]    
    #print(lines)    

    ########## zenity ##########
    res=zlist( ["lines"], lines )
    if res is None:
        print("q... nothing selected")
        quit()
    UMOUNT()        
    mou=res[0].split()[0]
    print("i... mounting {} to {}".format(mou,MOUNTPOINT))
    ### CMD ###
    MOUNT(mou)
    RUNXTERM()
    UMOUNT()

    

#=======================  notify-send =========
# ===  from ntpcheck

def set_environment():
    # i want unity or xfce4 - on p34
    CMD="pgrep -u "+os.environ['USER']+" xfce4|unity-panel"
    pid=subprocess.check_output( CMD.split() ).split()[0].decode("utf8").rstrip()
    print("I have PID", pid)
    CMD="grep -z DBUS_SESSION_BUS_ADDRESS /proc/"+pid+"/environ"
    dsba=subprocess.check_output( CMD.split()  ).decode("utf8").rstrip()
    dsba2=dsba.split("DBUS_SESSION_BUS_ADDRESS=")[1]
    print("I have DSBA ", dsba)
    print("I have DSBA2", dsba2)
    return dsba2

mydsba=set_environment()


def note( mess, col="" ):
    global mysdba
    ICOPA="/usr/share/icons/gnome/32x32/status/"
    ICOPA="/usr/share/icons/breeze/status/64/"
    CMD="notify-send -t 1 -i "+ICOPA
    if col=="green":
        CMD=CMD+"security-high.svg"
    elif col=="red":
        CMD=CMD+"security-low.svg"
    elif col=="yellow":
        CMD=CMD+"security-medium.svg"
    else:
        CMD=CMD+"dialog-question.vg"
        
    CMDL=CMD.split()
    CMDL.append(mess)
    subprocess.call( CMDL , env={"DBUS_SESSION_BUS_ADDRESS":mydsba} )

#======================== ENDOF NOTIFYSEND =================



def get_hostname():
    import socket
    return socket.gethostname()

def get_signature():
    import datetime
    r=get_hostname()
    r=r+"_"+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%a')
    return r


# def prune_repo(repo):
#     CMD='borg prune -v --list '
#     CMD=CMD+repo
#     CMD=CMD+' --prefix '+get_hostname()+' '
#     CMD=CMD+' --keep-within=7d --keep-weekly=4 --keep-monthly=-1 '
#     logger.infoC( CMD )
#     return


def load_addr_repo_pairs():
    global logger
    logger.info("going to INIT /load_repo_pairs/")
    li=[]
    try:
        with open(CONFIGFILE) as f:
            li=f.readlines()
    except:
        logger.error("NO FILE "+CONFIGFILE+' / quit')
        logger.error("file contains:  path_to_repo path_to_data4backup")
        quit()
    # clean lines
    li=[ i.strip() for i in li]
    # remove \n and comments
    li=[ i for i in li if len(i)>0 and i.strip()[0]!="#"]
    # divide into pairs
    li=[ i.split() for i in li]
    return li






def mail_out_results( SIG, ok, nokq , nok):
    global results
    texth=" OK="+str(ok)+" --="+str(nokq)+" BAD="+str(nok) 
    logger.infoP("mailing results: "+texth )
    texth=SIG+" "+texth
    # Create a text/plain message #    msg = MIMEText(fp.read())
    textb=""
    for i in results:
        textb=textb+"  ".join(i)+"\n"
    msg=MIMEText( textb + "\n\n\n--...no ping\nxx...error\n")
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
        logger.error("sshfs:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        logger.error("cannot unmount "+dest)
        countdown("problem",10)
        quit()





def flush_mysql( server_folder ):
    MODIR="~/BORGBACKUP/mount_mysql/"
    MODIR=os.path.expanduser(MODIR)
    if not os.path.isdir(MODIR):
        logger.error("I need to have "+MODIR+" to backup")
        CMD="mkdir -p "+MODIR
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        logger.infoP("directory "+CMD+" created")
        #quit()
    # directory created.....
    mysqls=glob.glob( os.path.expanduser("~/.*.mysql") )
    logger.info( "AvailableMySQLs: "+" ".join(mysqls) )
    allconf=[]
    CMD=""
    FROMPATH=MODIR+"all-databases_in_edie.mysql"
    for onesql in mysqls:
        with open( onesql ) as f:
            logger.infoC("mysql config readout: "+onesql)
            allconf=f.readlines()
        if allconf[0].rstrip()=="localhost":
            CMD= "mysqldump -u "+allconf[1].rstrip()+" -p"+allconf[2].rstrip()+" --all-databases > "+FROMPATH
            logger.info("preparing to flush mysql to: "+FROMPATH)
        else:
            logger.info("not localhost sql: ",onesql)
    #print( CMD )
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        return FROMPATH
    except subprocess.CalledProcessError as grepexc:
        logger.error("flushmysql:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        logger.error("cannot do mysqldump") # MOSTLY already EXist
        countdown("problem",10)
        return "xx"        

    
    
    
    
def mount_sshfs( server_folder):
    MODIR="~/BORGBACKUP/mount_sshfs/"
    MODIR=os.path.expanduser(MODIR)
    if not os.path.isdir(MODIR):
        logger.error("I need to have "+MODIR+" to backup")
        CMD="mkdir -p "+MODIR
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        logger.infoP("directory "+CMD+" created")
        #quit()
    CMD="sshfs "+server_folder+" "+MODIR
    logger.infoC( CMD )
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        logger.infoP("ok")
        logger.infoP(res)
    except subprocess.CalledProcessError as grepexc:
        logger.error("mountssh:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        logger.error("cannot init NEW borg REPO") # MOSTLY already EXist
        countdown("problem",10)
        return ""
        #quit()# no quit possible inside
    return MODIR




UNMOUNT_THESE=[]
def get_mountpoints(repo):
    global UNMOUNT_THESE
    with open("/etc/fstab") as f:
        lines=f.readlines()
    lines=[ x.rstrip() for x in lines if x[0]!="#"]
    mpoi=[ x.split()[1] for x in lines ]
    mpoi=[ x for x in mpoi if ( x.find("/mnt/")>=0 or x.find("/media")>=0 ) ]
    print(  mpoi )
    moun=[ x for x in mpoi if repo.find(x)>=0 ]
    if len(moun)>0:
        if os.path.ismount( moun[0] ):
            logger.info(repo+" is already mounted ... ")
            return 0
        else:
            logger.infoP("i try to mount"+moun[0])
            CMD="mount "+moun[0]
            reslist=subprocess.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
            UNMOUNT_THESE.append( moun[0] )
            return 1
    return 0


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
        logger.error("init:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        logger.error("cannot init NEW borg REPO")
        countdown("problem",10)
    return








def borg_create( repo , sig, directory ):
    '''
    borg create /path/to/repo::Monday ~/src ~/Documents 
    borg create -v --stats /path/to/repo::Tuesday ~/src ~/Documents
    '''
    ssh=False
    #====   ssh address (MyBookLive e.g.)
    # if not directory=> can be ssh:
    #                 => can be mysql:
    if directory.split(":")[0]=="mysql":
        logger.infoC("MYSQL                 ")
        res=flush_mysql( directory )
        if res=="xx": return res
        logger.info("mysql flushed into a temporary file "+res)
        directory=os.path.dirname(res)
        #####quit()
        ###return "ok"
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
            if directory=="": return "--"
        except subprocess.CalledProcessError as grepexc:
            #logger.error("error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
            logger.error("create:error code "+ str(grepexc.returncode) )
            logger.error("no host - no directory")
            return "--"
    # ===  try to "create" - but - a lock can appear here!!
    OPTIONS=" -v --stats -p --compression lzma,9 --info "
    CMD="borg create "+OPTIONS+" "+repo+"::"+sig+" "+directory
    logger.infoC( CMD )
    create_ok=False
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        logger.infoP("ok")
        logger.infoP(res)
        create_ok=True
    except subprocess.CalledProcessError as grepexc:
        logger.error("create2:error code "+ str(grepexc.returncode)+grepexc.output.decode('utf8'))
        logger.error("cannot create backup ..... maybe ....")
    if not create_ok:
        # === I try to break the lock  ======
        note("trying to BREAK BORG LOCK !","red")
        countdown("...  I TRY TO BREAK THE BORG FILE LOCK /maybe dangerous/ ...",15)
        CMDBREAK="borg break-lock "+repo
        res=subprocess.check_output( CMDBREAK, shell=True ).decode("utf8")
        try:
            res=subprocess.check_output( CMD, shell=True ).decode("utf8")
            # very extensive LOG
            logger.infoP("ok")
            logger.infoP(res)
            create_ok=True
        except subprocess.CalledProcessError as grepexc:
            logger.error("create3:error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
            logger.error("... even with break-lock ... cannot create")
    # ==== END OF CREATE ====
    if ssh:unmount_sshfs(directory)
    if not create_ok:
        countdown("ending this repo with a problem",10)
        return "xx"
    #logger.info( CMD )
    return "ok"



def borg_prune( repo , sig, directory ):
    """
    borg prune -v --list --keep-daily=7 --keep-weekly=4 --keep-monthly=-1 /path/to/repo
    """
    OPTIONS="  -v --list --keep-daily=10 --keep-weekly=4 --keep-monthly=-1 "
    CMD="borg prune "+OPTIONS+" "+repo
    logger.infoC( CMD )
    try:
        res=subprocess.check_output( CMD, shell=True ).decode("utf8")
        # very extensive LOG
        logger.infoP("ok")
        logger.infoP(res)
    except subprocess.CalledProcessError as grepexc:
            logger.error("prune:error code "+ str(grepexc.returncode) )
            logger.error("no host - no directory")
            


        
        

def borg_info( repo, stamp):
    """
    i dont remember- but borg info will show details about the REPO
    it will be put into LOG - so probably never seen again....
    ... could go to email
    """
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
    returns ""  -    repo ok BUT  no stamp present
    returns None  -  repo does NOT exist
    '''
    CMD="borg list  "+repo
    logger.infoC( CMD)
    try:
        reslist=subprocess.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
        logger.infoP("ok "+str(len(reslist)))
    except subprocess.CalledProcessError as grepexc:
        # deosnot exist ... error 2
        logger.error("list: error code "+ str(grepexc.returncode)+ grepexc.output.decode('utf8'))
        # try to mount ..... owncloud case 
        get_mountpoints(repo)
        return None
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

if mymod.args.list:
    logger.info("list only")
    for li in pairs:
        borg_list( li[0] )
    quit()

if mymod.args.mount:
    logger.info("mount /mc /fusermount -u  only")
    MOUNTUMOUNT()
    quit()

results=[]
ok=0
nokq=0 # -- ping
nok=0  # error
for li in pairs:
    logger_head.infoX("=============================================================")
    if len(li)<2:
        logger.error("BAD INPUT LINE ... STOPPING")
        break
    logger_head.infoX( "about to backup : "+li[1] )
    logger_head.infoX( "    into repo   : "+li[0] )
    last=borg_list( li[0] ) 
    if last==None:
        countdown("initialize new repository?",5)
        if not os.path.exists( li[0] ):
            try:
                os.makedirs( li[0] )
            except:
                logger.error("Cannot create a directory "+li[0] )
                results.append( ["xx",li[1]+"--->"+li[0] ]  )
                note(li[0]+" [xx]","red")
                nok=nok+1
                continue  # ? next item in pairs ?
            borg_init( li[0] )
        last=""
    if last is "": # empty line
        logger.warning("there was empty line in repo ... probably totaly new repo")
        #countdown("there was empty line in repo",3)
        #continue
    logger_head.infoC(last+" ==> "+SIGNATURE)
    countdown("create new backup now?",8)
    res=borg_create( li[0], SIGNATURE , li[1] )
    # added 20171002 - pruning -leave 10days,
    borg_prune( li[0], SIGNATURE , li[1] )
    results.append( [res,li[1]+"--->"+li[0] ]  )
    #print( results )
    if res=="ok":
        borg_info(li[0], SIGNATURE)
        ok=ok+1
        note(li[0]+" [ok]","green")
    elif res=="--":
        nokq=nokq+1
        note(li[0]+" [--]","yellow")
    else:
        nok=nok+1
        note(li[0]+" [xx]","red")
##########################################
mail_out_results(SIGNATURE, ok, nokq, nok )
print( results )
for qq in results:
    print(qq,"\n")
for x in UNMOUNT_THESE:
    logger.info("fusermount -u "+x)
    CMD="fusermount -u "+x
    res=subprocess.check_output( CMD.split() )#.split()[0].decode("utf8").rstrip()
    #print(res)
