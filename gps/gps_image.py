import tkinter_loop
from staticmap import StaticMap, CircleMarker, Line
from math import ceil  # reduce # markers

from gps_socket import translate_gps_line, gps_info, set_gps_info
import gps_socket
import datetime



from tkinter_loop import IMX,IMY
### PIL for printing on png file
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


# to use get_text with radius
#from math import floor,cos,sin
from math import sqrt,cos,sin,pi,floor,asin,radians

LAST_IMAGE=0
TRACK_LIST=[]
TARGET_LIST=[]
POI_LIST=[]


delta_img_draw=0.0 # time to draw the map
gps_start_time=0.0
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



    
def load_target_log():
    global TARGET_LIST
    print("LOADING TARGET TRACK")
    lines=[]
    try:
        with open("gps_target.log", "r" ) as f:
            lines=f.read().rstrip().split("\n")
    except:
        print("NO TARGET TACK    gps_target.log")
    print( "\nNumber of lines in TARGET:", len(lines) )
    for li in lines:
        x,y=float(li.split()[2].strip()),float(li.split()[3].strip())
        TARGET_LIST.append(  (x,y)  )
    #print( TARGET_LIST )


def load_track_log():
    global TRACK_LIST
    print("LOADING TRACK")
    lines=[]
    try:
        with open("gps_track.log", "r" ) as f:
            lines=f.read().rstrip().split("\n")
    except:
        print("NO TRACK TO LOAD")
    print( "\nNumber of lines in TRACK:", len(lines) )
    totdist=0.0
    for li in lines:
        x,y=float(li.split()[2].strip()),float(li.split()[3].strip())
        TRACK_LIST.append(  (x,y)  )
        totdist=float( li.split()[9].strip() )
    print( "============== PRESET TOT DIST ",gps_info['disttot'],"->",totdist )
    #### NW gps_info['disttot']=totdist
    set_gps_info( totdist )
    #gps_socket.gps_info['distttot']=totdist   # i want to continue with
    #gps_socket.gps_info['distttot']=444.444
    #gps_info['distttot']=totdist
    print( "============== PRESET TOT DIST ", gps_info['disttot'] )
    gps_info['XCoor']=TRACK_LIST[-1][0]
    gps_info['YCoor']=TRACK_LIST[-1][1]





def gps_text(image,pos,text,fg='black',bg='white',radius=1.0):
    global DEBUG
    if DEBUG:print("DEBUG","entered gettext")
    global IMX
    global IMY
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
            posi=(1,IMY-h)
        if (pos=='rt'):
            posi=(IMX-w-2,1)
        if (pos=='rb'):
            posi=(IMX-w-2,IMY-h)
    else:
        if DEBUG: print("DEBUG",text,'course to ',pos)
        tox=IMX/2+sin(pos/180*pi)*IMX/2*radius
        toy=IMY/2-cos(pos/180*pi)*IMY/2*radius
        # shift the tox toy
        tox=int(tox-w/2)
        toy=int(toy-h/2)
        if (tox+w)>IMX: tox=IMX-w-1
        if (tox)<0:   tox=1
        if (toy+h)>=IMY: toy=IMY-h
        if (toy)<0:   toy=1
#        if ( sin(pos)>=0):
#            tox=tox-w
#        if (cos(pos)>0):
#            toy=toy-h
#        posi=( int(tox), int(toy) )
        posi=( tox, toy )
         
    if DEBUG: print('DEBUG','120=', w,h, posi, IMX,IMY)
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
    if realdelay>0 and realdelay<100000:
    #if realdelay>gps_info['utcdelay']:
        #if gps_info['utcdelay']==-1.0:
        #    print("======== CLOCK DELAY SET: ", realdelay)
        #    gps_info['utcdelay']=realdelay
        print("...  --- make_img delayed to gps clock: ", realdelay, 's.', '{:.2f} s. to draw'.format(delta_img_draw))
        if not fast_response and  realdelay>2 and realdelay<1000000:print("!... verify /etc/ntp.conf for GPS")
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

    
        
    #========== CONTINUE WITH A TRACK LOG
    TRACK_LIST.append(  (gps_info['XCoor'] , gps_info['YCoor'] )  )

    
    #print("--- from the LAST_IMAGE   =",(start-LAST_IMAGE).microseconds/1e6,
    #      "RT delay=",realdelay)
    # MAYBE NO MARKER NEEDED
    #if gps_info['fix']=='+' and gps_info['dist']>0.:




    
    ######################
    #======== COMPLETELU NEW MARKS ALWAYS
    tkinter_loop.m1.markers=[]

    #========  IS TARGET = NAVIGATION
    for coor in TARGET_LIST:
        mam=CircleMarker( coor, 'blue', 3)
        #print( coor)
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
    gps_text(tkinter_loop.tk_image,'lb',"{}  {:.1f} km".format(strfdelta(start-gps_start_time,"%H:%M:%S"), gps_info['disttot']) )
    ##### TIME
    #gps_text(tkinter_loop.tk_image,'rb',gps_info['timex'])
    
    gps_text(tkinter_loop.tk_image,'rb', start.strftime("%H:%M:%S"))








    
    stop=datetime.datetime.now()
    delta=stop-start
    delta_img_draw=delta.seconds + (float(1) * delta.microseconds/1e6)  
    LAST_IMAGE=stop # reset LAST_IMAGE coiunter to reduce CPU
    LAST_IMAGE=start # reset LAST_IMAGE coiunter to reduce CPU
    #============DEBUG
    #print("\nimg:", delta_img_draw, "marks=",ltr ,end="\n")

    
