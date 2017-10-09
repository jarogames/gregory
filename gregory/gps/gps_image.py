import gregory.gps.tkinter_loop as tkinter_loop
from staticmap import StaticMap, CircleMarker, Line
from math import ceil  # reduce # markers

from gregory.gps.gps_socket import translate_gps_line, gps_info, set_gps_info,get_dist_prec
import gregory.gps.gps_socket
import datetime
from datetime import timedelta


from gregory.gps.tkinter_loop import IMX,IMY,getIMX,getIMY
### PIL for printing on png file
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


# to use get_text with radius
#from math import floor,cos,sin
from math import sqrt,cos,sin,pi,floor,asin,radians,pow


from functools import reduce

import  gregory.gps.sunposition as sunposition
LAST_IMAGE=0
TRACK_LIST=[]
TARGET_LIST=[]
POI_LIST=[]

def reset_TRACK_LIST():
    global TRACK_LIST
    TRACK_LIST=[]


# display SUN/MOON
SUNMOONv=False
def SUNMOON():
    global SUNMOONv
    SUNMOONv=not SUNMOONv
    return SUNMOONv

#display watch time of gps_target.log
WATCHTIMEv=False
def WATCHTIME():
    global WATCHTIMEv
    WATCHTIMEv=not WATCHTIMEv
    return WATCHTIMEv

def reset_gps_start_time():
    global  gps_start_time
    gps_start_time=datetime.datetime.now()-timedelta(seconds=0) # this should also go to TRACK FILE

reset_gps_start_time()    
delta_img_draw=0.0 # time to draw the map
DEBUG=False


def takespread(sequence, num):
    '''
    just select every 2nd point - in generat it could be more complex
    '''
    return sequence[0::2]


# - this is or formating timedelta
from string import Template

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

#def strfdelta(tdelta, fmt):
#    d = {"D": tdelta.days}
#    d["H"], rem = divmod(tdelta.seconds, 3600)
#    d["M"], d["S"] = divmod(rem, 60)
#    t = DeltaTemplate(fmt)
#    return t.substitute(**d)







def load_poi_log():
    global POI_LIST
    POI_LIST=[]
    print("LOADING POI ")
    lines=[]
    try:
        with open("gps_POI.log", "r" ) as f:
            lines=f.read().rstrip().split("\n")
    except:
        print("NO POI TACK")
    print( "\nNumber of lines in POI:", len(lines) )
    for li in lines:
        if len(li.split())>5:
            x,y,word=float(li.split()[2].strip()),float(li.split()[3].strip()),li.split()[-1]
            POI_LIST.append(  (x,y,word)  )
    #print( POI_LIST )




#############
# i will need to decode trak log 00:00:05  ->  5
#                decode target time also 
#
def get_sec(time_str):
    h, m, s = time_str.split(':')
    de= int(h) * 3600 + int(m) * 60 + int(s)
    #print(de,'seconds')
    return de



    
##############################
#  this is the planned route track:
#
#   usually from GraphHopper  with API key
#
def load_target_log():
    global TARGET_LIST
    print("LOADING TARGET TRACK")
    lines=[]
    try:
        with open("gps_target.log", "r" ) as f:
            lines=f.read().rstrip().split("\n")
    except:
        print("NO TARGET TACK    gps_target.log")
    ## if lines < than 2
    if len(lines)<2:
        return
    print( "\nNumber of lines in TARGET:", len(lines) )
    ## if some lines have ---- or #comment
    for li in lines:
        if len(li.split())>4:
            x,y=float(li.split()[2].strip()),float(li.split()[3].strip())
            tim=int( get_sec(li.split()[0]) )
            TARGET_LIST.append(  (x,y,tim)  )
            
    #--- measure the distance in gps_tareget.log
    trackdist=0.0
    for p in range(len(TARGET_LIST)-1):
        a=TARGET_LIST[p][0]
        b=TARGET_LIST[p][1]
        x=TARGET_LIST[p+1][0]
        y=TARGET_LIST[p+1][1]
        trackdist=trackdist+ get_dist_prec(a,b,x,y)
        #print(trackdist, a, b )
    print("TRACK DIST=", trackdist)
    set_gps_info('trkdist', trackdist )


    
    

    
def load_track_log():
    global TRACK_LIST
    global gps_start_time 

    print("LOADING TRACK")
    lines=[]
    try:
        with open("gps_track.log", "r" ) as f:
            lines=f.read().rstrip().split("\n")
    except:
        print("NO TRACK TO LOAD")
        return
    print( "\nNumber of lines in TRACK:", len(lines) )
    totdist=0.0
    LASTACTTIME="00:00:00"
    if len(lines)<2:
        return
    for li in lines:
        if len(li.split())>9:
            x,y=float(li.split()[2].strip()),float(li.split()[3].strip())
            LASTACTTIME=li.split()[0].strip()
            TRACK_LIST.append(  (x,y)  )
            totdist=float( li.split()[9].strip() )
            #print(totdist)
    print( "============== PRESET TOT DIST ",gps_info['disttot'],"->",totdist )
    #### NW gps_info['disttot']=totdist
    set_gps_info( 'disttot', totdist )
    #gps_socket.gps_info['distttot']=totdist   # i want to continue with
    #gps_socket.gps_info['distttot']=444.444
    #gps_info['distttot']=totdist
    print( "============== PRESET TOT DIST ", gps_info['disttot'] )
    gps_info['XCoor']=TRACK_LIST[-1][0]
    gps_info['YCoor']=TRACK_LIST[-1][1]
    gps_info['acttime']=LASTACTTIME
    print( "======== acttime ",gps_start_time, "tracklist=" , LASTACTTIME )
    gps_start_time=gps_start_time - datetime.timedelta( seconds=get_sec( LASTACTTIME ) )
    
    #gps_start_time=gps_start_time-datetime.timedelta( seconds=9 )
    print("=============== PRESET TIME ", gps_start_time )
    




    

#######################
#
#    SUN 
#

def gps_circle( image , pos ,text , tcolor, radius=1.0):
    global DEBUG
    #DEBUG=True
    if DEBUG:print("DEBUG","entered gettext")
    #global IMX
    #global IMY
    draw = ImageDraw.Draw(image, 'RGBA')
    font22   = ImageFont.truetype("Ubuntu-B.ttf", 22)
    font14 = ImageFont.truetype("Ubuntu-B.ttf", 14)
    font=font22
    if isinstance(pos, str):
        font=font22
    else:
        font=font14
    w, h = draw.textsize(text, font)
    posi=(1,1)
    if DEBUG: print("DEBUG",'isinstantce str ')
    if DEBUG: print("DEBUG",text,'course to ',pos)
    tox=getIMX()/2+sin(pos/180*pi)*getIMY()/2*radius  # IMY here
    toy=getIMY()/2-cos(pos/180*pi)*getIMY()/2*radius
    # shift the tox toy
    tox=int(tox-w/2)
    toy=int(toy-h/2)
    if (tox+w)>getIMX(): tox=getIMX()-w-1
    if (tox)<0:   tox=1
    if (toy+h)>=getIMY(): toy=getIMY()-h
    if (toy)<0:   toy=1
    #        if ( sin(pos)>=0):
    #            tox=tox-w
    #        if (cos(pos)>0):
    #            toy=toy-h
    #        posi=( int(tox), int(toy) )
    posi=( tox, toy )
    posf=( posi[0]+w , posi[1]+h )
    draw.rectangle( [posi,posf] , (0,0,0,110)  ) #grey dark rect
    draw.text( posi, text ,        tcolor  , font=font)
    #draw.text( posi, "MOON",         (255,115,0,100) , font=font)
    #draw.text( posi, text,         (0,200,200,100) , font=font)
    draw.ellipse( (5 +getIMX()/2-getIMY()/2, 5, getIMX()/2+getIMY()/2-5, getIMY()-5), fill =None, outline ='black')




    

    

def gps_text(image,pos,text,fg='black',bg='white',radius=1.0):
    global DEBUG
    if DEBUG:print("DEBUG","entered gettext")
    #global IMX
    #global IMY
    draw = ImageDraw.Draw(image, 'RGBA')
    font22   = ImageFont.truetype("Ubuntu-B.ttf", 22)
    font14 = ImageFont.truetype("Ubuntu-B.ttf", 14)
    font=font22
    if isinstance(pos, str):
        font=font22
    else:
        font=font14
    w, h = draw.textsize(text, font)
    posi=(1,1)
    if DEBUG: print("DEBUG",'isinstantce str ')
    if isinstance(pos, str):
        if DEBUG: print('str ...', pos)
        if (pos=='lt'):
            posi=(1,1)
        if (pos=='lb'):
            posi=(1,getIMY()-h)
        if (pos=='rt'):
            posi=(getIMX()-w-2,1)
        if (pos=='rb'):
            posi=(getIMX()-w-2,getIMY()-h)
    else:
        if DEBUG: print("DEBUG",text,'course to ',pos)
        tox=getIMX()/2+sin(pos/180*pi)*getIMX()/2*radius
        toy=getIMY()/2-cos(pos/180*pi)*getIMY()/2*radius
        # shift the tox toy
        tox=int(tox-w/2)
        toy=int(toy-h/2)
        if (tox+w)>getIMX(): tox=getIMX()-w-1
        if (tox)<0:   tox=1
        if (toy+h)>=getIMY(): toy=getIMY()-h
        if (toy)<0:   toy=1
#        if ( sin(pos)>=0):
#            tox=tox-w
#        if (cos(pos)>0):
#            toy=toy-h
#        posi=( int(tox), int(toy) )
        posi=( tox, toy )
         
    if DEBUG: print('DEBUG','120=', w,h, posi, getIMX(),getIMY())
    posf=( posi[0]+w , posi[1]+h )
    whitefog=(255, 255, 255, 110)
    blackfog=(0, 0, 0, 110)
    redfog=(255,0,0,  110)
    greenfog=(0,125,0,  110)
    bluefog=(0,0,125,  110)
    white=(255,255,255)
    black=(0,0,0)
    red=(255,0,0)
    green=(0,255,0)
    ##### SPEED
    #text="{:4.1f}".format(speed*1.852)+' km/h'
    if fg=='black': fcol=black
    if fg=='white': fcol=white
    if fg=='red':   fcol=red
    if fg=='green': fcol=green
    ##########################
    if bg=='black': bcol=blackfog
    if bg=='white': bcol=whitefog
    if bg=='red':   bcol=redfog
    if bg=='green': bcol=greenfog
    if bg=='blue': bcol=bluefog
    draw.rectangle( [posi,posf] , bcol )
    draw.text( posi,text,         fcol , font=font)
    if DEBUG: print('DEBUG','rectg and text ok')











########################################################
#
#
##############################
#
#                IMAGE
#
##############################
#
#
#######################################################

    
def make_image(  fast_response=False ):
    global TRACK_LIST
    global TARGET_LIST
    global DEBUG
    global delta_img_draw
    global gps_start_time
    #MAP
    global LAST_IMAGE
    
    utc=int( datetime.datetime.utcnow().strftime("%s") )
    start=datetime.datetime.now()
    if gps_start_time==0:
        gps_start_time=start
    if LAST_IMAGE==0:
        print("...  First image - setting the LAST_IMAGE time")
        LAST_IMAGE=start
        return
    ########################################
    # creating image takes 0.5-1 sec or more
    #   i will not check 1 img/sec
    #  BUT tricky - i check a delay a skip all delayed
    ##
    delta_ss=(start-LAST_IMAGE).seconds+(start-LAST_IMAGE).microseconds/1e+6
    #print("...", delta_ss)
    if not fast_response and delta_ss<0.95:
        #DEBUG
        #print("...  i wait for 0.95 ms - i have ",delta_ss)
        return


    
    #############################
    # if pc clock is delayed ret immediat
    #  now I have ntp related to GPS --------
    #
    realdelay=utc - gps_info['utc']
    if realdelay>0 and realdelay<10000:
    #if realdelay>gps_info['utcdelay']:
        #if gps_info['utcdelay']==-1.0:
        #    print("======== CLOCK DELAY SET: ", realdelay)
        #    gps_info['utcdelay']=realdelay
        print("\n...  --- make_img delayed to gps clock: ", realdelay, 's.', '{:.2f} s. to draw'.format(delta_img_draw))
        if not fast_response and  realdelay>2 and realdelay<10000:print("!... verify /etc/ntp.conf for GPS")
        return
   # print("{:4.0f} ms\n".format((start-LAST_IMAGE).microseconds/1000) )




   
    #==== REDUCE NUMBER OF POINTS =====
 
    ltr=len(TRACK_LIST)
    ltg=len(TARGET_LIST)
    #print("===================== TRACK_LIST  HAS", ltr)
    #print("===================== TARGET_LIST HAS", ltg)
    while ltr>3000:
        TRACK_LIST=takespread(TRACK_LIST,2 )
        ltr=len(TRACK_LIST)
    while ltg>3000:
        TARGET_LIST=takespread(TARGET_LIST,2 )
        ltg=len(TARGET_LIST)
    #print("===================== TRACK_LIST  HAS", ltr)
    #print("===================== TARGET_LIST HAS", ltg)

    
        
    #========== CONTINUE WITH A TRACK LOG === APPEND to LIST
    TRACK_LIST.append(  (gps_info['XCoor'] , gps_info['YCoor'] )  )

    
    #print("--- from the LAST_IMAGE   =",(start-LAST_IMAGE).microseconds/1e6,
    #      "RT delay=",realdelay)
    # MAYBE NO MARKER NEEDED
    #if gps_info['fix']=='+' and gps_info['dist']>0.:




    
    ######################
    #======== COMPLETELU NEW MARKS ALWAYS
    tkinter_loop.m1.markers=[]

    #========  IS TARGET = NAVIGATION
    closetarg=100000
    tgtag=(0,0,0)
    for coor3 in TARGET_LIST:
        coor=(coor3[0],coor3[1]) # [2] is time in seconds
        mam=CircleMarker( coor, 'blue', 3)
        #print( coor)
        tkinter_loop.m1.add_marker(mam)
        # compute closest point to XYCoor
        ct2=get_dist_prec(gps_info['XCoor'],gps_info['YCoor'],
                          coor[0],coor[1] )
        #ct2=pow(gps_info['XCoor']-coor[0],2) + pow(gps_info['YCoor']-coor[1],2)
        if (ct2<closetarg):
            closetarg=ct2
            tgtag=coor3

    # special mode - d pressed - plot closest point
    if WATCHTIMEv:  # compare the target points with gps
        print("closest target: {} {:.1f} km".format( tgtag,closetarg ) )
        mam=CircleMarker( tgtag, 'red', 7)
        tkinter_loop.m1.add_marker(mam)
        mam=CircleMarker( tgtag, 'white', 5)
        tkinter_loop.m1.add_marker(mam)



        
    #========  IS OLD TRACK
    for coor in TRACK_LIST:
        mam=CircleMarker( coor, 'orange', 3)
        #print( coor )
        tkinter_loop.m1.add_marker(mam)

        #========  IS POI
    for coor3 in POI_LIST:
        coor=( coor3[0],coor3[1])
        if coor3[2]=='yellow' or\
           coor3[2]=='white' or\
           coor3[2]=='orange' or\
           coor3[2]=='red' or\
           coor3[2]=='pink' or\
           coor3[2]=='green' or\
           coor3[2]=='lightgreen' or\
           coor3[2]=='blue'  or\
           coor3[2]=='magenta'  or\
           coor3[2]=='grey'  or\
           coor3[2]=='lightgray':
            incol=coor3[2]
        else:
            incol='black'
        mam=CircleMarker( coor, 'black', 7)
        tkinter_loop.m1.add_marker(mam)
        mam=CircleMarker( coor, incol , 5)
        tkinter_loop.m1.add_marker(mam)
        #print( coor)



    #======== RED IS ACTUAL GAME
    mam=CircleMarker( (gps_info['XCoor'],gps_info['YCoor']),'red', 7)
    tkinter_loop.m1.add_marker(mam)



    #print("... RENDERING")    
    #======== RENDER============#####################
    failrender=True
    while failrender:
        try:
            tkinter_loop.tk_image=tkinter_loop.m1.render(zoom=tkinter_loop.tk_zoomset[ tkinter_loop.tk_zoom],center=(gps_info['XCoor']+gps_info['XOffs'],gps_info['YCoor']+gps_info['YOffs'] )   )
            failrender=False
        except:
            if tkinter_loop.tk_zoom>0: tkinter_loop.tk_zoom=tkinter_loop.tk_zoom-1


            
            
    if WATCHTIMEv:  # display (if d was pressed) time difference
        QQ1=start-gps_start_time - timedelta(seconds=tgtag[2])
        print("QQ=", QQ1.seconds)
        if QQ1.seconds>40000:
            QQ=strfdelta( timedelta(seconds=3600*24-QQ1.seconds) ,"%H:%M:%S")
            gps_text( tkinter_loop.tk_image, 0 ,"D={}   {:.1f}".format(QQ,closetarg), fg='white',bg='green',radius=0.7)        

        else:
            QQ=strfdelta( QQ1,"%H:%M:%S")
            gps_text( tkinter_loop.tk_image, 0 ,"D={}   {:.1f}".format(QQ,closetarg), fg='white',bg='red',radius=0.7)        


        

    ##### PRINT  LABELS TO CORNERS #####        
    ##### DISTTOT
    #gps_text( tkinter_loop.tk_image, 90 ,"{:5.1f}".format(gps_info['disttot'])+' km', fg='white',bg='black',radius=1.0)
    ##### SPEED
    gps_text( tkinter_loop.tk_image,'lt',"{:4.1f} km/h  {} m".format(gps_info['speed']*1.852,gps_info['altitude'] ) )
    ##### HEADING
    if gps_info['fix']=="+":
        gps_text(tkinter_loop.tk_image,'rt',"{:3.0f}".format(gps_info['course']))
    else:
        gps_text(tkinter_loop.tk_image,'rt','NO FIX',fg='red',bg='black')
    ##### Altitude /// go time + dist
    gps_text(tkinter_loop.tk_image,'lb',"{}  {:.1f} km/{:.0f}".format(strfdelta(start-gps_start_time,"%H:%M:%S"), gps_info['disttot'], gps_info['trkdist']) )
    ##### TIME
    #gps_text(tkinter_loop.tk_image,'rb',gps_info['timex'])

    # actual time (value of     start )
    gps_text(tkinter_loop.tk_image,'rb', start.strftime("%H:%M:%S"))

    # here i just define what is written
    gps_info['acttime']=strfdelta(start-gps_start_time,"%H:%M:%S")

    
    if SUNMOONv:
        LAT=gps_info['YCoor'] #37.6287
        LON=gps_info['XCoor'] #15.1749
        now = datetime.datetime.utcnow()
        res = sunposition.observed_sunpos(now,LAT,LON, gps_info['altitude'])[:2] #discard RA, dec, H
        print("\nSUN position:",res)
        suncol=(255,255,0,255) #yellow
        # sunrise # sunset
        #degmax,degmin=5,-2
        #if res[1]<degmax and res[1]>degmin:
        #    green=int(  (res[1]-degmin)/(degmax-degmin)*255)
        #    suncol=(255,green,0,255)
        degmax,degmin=92,85
        if res[1]<degmax and res[1]>degmin:
            green=int(  (degmax-res[1])/(degmax-degmin)*150+104 )
            suncol=(255,green,0,255)
            #print(suncol)
        #night    
        if res[1]<=-2 or res[1]>92: suncol=(25,25,25,255)
        
        gps_circle(tkinter_loop.tk_image, res[0] ,"SUN {:.2f}".format(res[1]),
                   suncol, radius=1.0  )





    
    stop=datetime.datetime.now()
    delta=stop-start
    delta_img_draw=delta.seconds + (float(1) * delta.microseconds/1e6)  
    LAST_IMAGE=stop # reset LAST_IMAGE coiunter to reduce CPU
    LAST_IMAGE=start # reset LAST_IMAGE coiunter to reduce CPU
    #============DEBUG
    #print("\nimg:", delta_img_draw, "marks=",ltr ,end="\n")

    
