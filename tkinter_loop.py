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
tk_zoom=0
tk_zoomset=[]
tk_n=0
tk_command=None
tk_registered=False

def monitor_size():
    CMD="xrandr  | grep \* | cut -d' ' -f4"
    p=subprocess.check_output(CMD , shell=True)
    wihe=p.decode('utf8').rstrip().split('x')
    wihe=list(map(int,wihe))
    return wihe


#######################################
#  KEYPRESS
#######################################
def keydown(e):
    global tk_registered
    global tk_command
    print('keypressed')
    ###########
    tk_command=None
    if len(e.char)==0: return 
    print('     keypress /'+e.char+'/')
    if e.char==' ':
        key1="SPACE"
        print(key1)
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
    frame.focus_set()
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
    print("loop",tk_n,tk_command)
    tk_n=tk_n+1
    #if gps_info['fix']=='+' and gps_info['dist']>0.:
    if not tk_image is None:
        image=tk_image.resize( (int(IMX* resizeF) , int(IMY*resizeF) ) )
        tkimg = ImageTk.PhotoImage(image)
        tk_label.config(image=tkimg)
    if not tk_command is None:
        #############
        key1=tk_command
        consumer_id=7 # tkinter will have 7
        work_message =  { 'client' : consumer_id, 'cmd' : key1}
        print("i... sendin zmq keypress")
        tk_zmq_socket.send_json(work_message)
        print("i... keypress sent")

    if tk_command=='quit' or tk_command=="q":
        print('x... tk_root to quit..........')
        tk_root.quit()
        print('x... tk_root quitted')
        return
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
    tk_frame = tkinter.Frame(tk_root, width=100, height=100)
    tk_frame.bind("<Key>", keydown)
    tk_frame.bind("<Button-1>", callback)
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
print("============")
IMX,IMY=320,240
#IMX,IMY=640,480
#IMX,IMY=monitor_size()
resizeF=2
IMX=int(IMX/resizeF)-20
IMY=int(IMY/resizeF)-20
m1 = StaticMap( IMX,IMY, url_template='http://localhost:8900/{z}/{x}/{y}.png')
tk_zoomset=[5,8,12,15]   # zoom  0,1,2
##### 0 1 2 - it parses allowed zoomset
tk_zoom=2

if __name__ == "__main__":
    print("i... i am in main")
    
    ## this i want to be elsewhere....
    mam= CircleMarker( (gps_info['XCoor'],gps_info['YCoor']),'red', 1)
    m1.add_marker(mam)
    tk_image=m1.render(zoom=tk_zoomset[tk_zoom] , center=(gps_info['XCoor'] , gps_info['YCoor'] )   )
    tk_init()
    tk_root.mainloop()
