#!/usr/bin/python3
import tkinter
from PIL import Image, ImageTk
from gps_socket import gps_info
import staticmap
import subprocess
from staticmap import StaticMap, CircleMarker, Line
import time
import zmq


tk_root=None
tk_label=None
tk_frame=None
tk_image=None #this will be the IMAGE
tk_zoom=None
tk_zoomset=[]
tk_n=0
tk_command=None
tk_registered=False

##############################################
# monitor size
##############################################
def monitor_size():
    CMD="xrandr  | grep \* | cut -d' ' -f4"
    p=subprocess.check_output(CMD , shell=True)
    print("==========", p)
    wihe=p.decode('utf8').split()[0].rstrip().split('x')
    wihe=list(map(int,wihe))
    print("i... monitor size ",wihe)
    return wihe


#######################################
#  KEYPRESS
#######################################

def leftKey(event):
    global tk_registered
    global tk_command
    print( "Left key pressed")
    key1="LEFT"
    tk_command="LEFT"
        
def rightKey(event):
    global tk_registered
    global tk_command
    print( "Right key pressed")
    key1="RIGHT"
    tk_command="RIGHT"

def upKey(event):
    global tk_registered
    global tk_command
    print( "up key pressed")
    key1="UP"
    tk_command="UP"
        
def downKey(event):
    global tk_registered
    global tk_command
    print( "Down key pressed")
    key1="DOWN"
    tk_command="DOWN"


def keydown(e):
    global tk_registered
    global tk_command
    print('tkinter keypress')
    ###########
    tk_command=e.char
    if len(e.char)==0: return 
    print('     keypress /'+e.char+'/', len(e.char) )
    if e.char==' ':
        key1="SPACE"
        print(key1)
    if e.char=='\n':
        key1="ENT"
        print('backslash n')
    if e.char=='\r':
        key1="ENT"
        print('backslash r')
        tk_command="ENT"
    if e.char in ['q']:
        print('should be QUITTING...')
        tk_command='quit'
        key1='quit'
        print(key1)
    ##zmq_socket.close()
    
########
    return

################################## 
#     MOUSE 
##################################
def callback(event):
    global m1
    global tk_frame
    tk_frame.focus_set()
    print( "clicked at", event.x, event.y,"  ")
    print( m1._x_to_lon(m1._px_to_x(), zoom ) )


    
#############################################
# LOOP
#############################################
tk_zmq_socket=None
def tk_loop():
    global zoom
    global tk_root,tk_label,tk_frame,tk_n,tk_image,tk_command
    global tk_zmq_socket
    global resizeF,IMX,IMY
    #print("loop",tk_n,tk_command)
    tk_n=tk_n+1
    #if gps_info['fix']=='+' and gps_info['dist']>0.:
    if not tk_image is None:
        print("resize:",resizeF,IMX,IMY)
        image=tk_image.resize( (int(IMX* resizeF) , int(IMY*resizeF) ) )
        tkimg = ImageTk.PhotoImage(image)
        tk_label.config(image=tkimg)
    if not tk_command is None:
        #############
        key1=tk_command
        consumer_id=7 # tkinter will have 7
        work_message =  { 'client' : consumer_id, 'cmd' : key1}
        #print("i... sendin zmq keypress")
        tk_zmq_socket.send_json(work_message)
        #print("i... keypress sent")

    if tk_command=='quit' or tk_command=="q":
        print('x... tk_root to quit..........')
        tk_root.quit()
        print('x... tk_root quitted')
        return
    tk_command=None
    tk_root.update_idletasks()
    tk_root.after( 2, tk_loop )
    time.sleep( 0.35 )  # sleep here to leave it displayed


    

def tk_init():
    global tk_root,tk_label,tk_frame,tk_image
    global tk_zmq_socket,tk_registered
    ###########
    context = zmq.Context()
    tk_zmq_socket = context.socket(zmq.PUSH)
    tk_zmq_socket.connect("tcp://127.0.0.1:5558")
    if not tk_registered:
        key1='register'
        consumer_id=7 # tkinter will have 7
        work_message =  { 'client' : consumer_id, 'cmd' : key1}
        tk_zmq_socket.send_json(work_message)
        print("i... registration sent")
        tk_registered=True
    ##############
    tk_root = tkinter.Tk()
    tk_label = tkinter.Label( tk_root )
    ######label.bind("<KeyPress>", keydown)
    tk_label.pack()
    tk_frame = tkinter.Frame(tk_root, width=IMX, height=IMY)
    tk_frame.bind("<Key>", keydown)
    tk_frame.bind("<Button-1>", callback)
    tk_frame.bind('<Left>', leftKey)
    tk_frame.bind('<Right>', rightKey)
    tk_frame.bind('<Down>', downKey)
    tk_frame.bind('<Up>', upKey)
    tk_frame.pack()
    tk_frame.focus_set()
    img = None
    tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.
    print('worTKI: ... ... i wait with TKINTER ON')
    tk_loop()
    #tk_root.mainloop()


    
#############################################################
#
####
#
#############################################################
#print("============")
IMX,IMY=320,240
#IMX,IMY=640,480
IMX_ORI,IMY_ORI=monitor_size()
resizeF=1

#def set_resizeF(fac):
#    global resizeF
#    resizeF=fac
###set_resizeF(2)

def recalc_screen_size( resizeF1):
    global IMX,IMY,IMX_ORI,IMY_ORI, resizeF
    global m1
    IMX=int(IMX_ORI/resizeF1)-20
    IMY=int(IMY_ORI/resizeF1)-20
    resizeF=resizeF1
    m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png')
    #print()
recalc_screen_size(2)

tk_zoomset=[5,8,12,15]   # zoom  0,1,2
##### 0 1 2 - it parses allowed zoomset
tk_zoom=None

if __name__ == "__main__":
    print("i... i am in main")
    if tkinter_loop.tk_zoom==None: tkinter_loop.tk_zoom=0
 
    ## this i want to be elsewhere....
    mam= CircleMarker( (gps_info['XCoor'],gps_info['YCoor']),'red', 1)
    m1.add_marker(mam)
    tk_image=m1.render(zoom=tk_zoomset[tk_zoom] , center=(gps_info['XCoor'] , gps_info['YCoor'] )   )
    tk_init()
    tk_root.mainloop()
