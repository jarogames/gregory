import tkinter_loop
from staticmap import StaticMap, CircleMarker, Line
from math import ceil  # reduce # markers

from gps_socket import translate_gps_line, gps_info



def takespread(sequence, num):
    length = float(len(sequence))
    for i in range(num):
        return sequence[int(ceil(i * length / num))]


def load_track_log():
    print("LOADING TRACK")
    with open("gps_track.log", "r" ) as f:
        lines=f.read().rstrip().split("\n")
    print( "\nNumber of lines in TRACK:", len(lines) )
    for li in lines:
        #print(li)
        #print( li.split() )
        x,y=li.split()[2],li.split()[3]
        mam= CircleMarker( (x,y),'red', 3)
        tkinter_loop.m1.add_marker(mam)
    limark=list(tkinter_loop.m1.markers)

    print("\n\n\n",  limark[:5])
    # while len( limark )>1000:
    #     tkinter_loop.m1.markers=takespread(tkinter_loop.m1.markers,
    #                                        int(len(limark)/2) )
    #     limark=list(tkinter_loop.m1.markers)
    
def make_image():
    #MAP
    # MAYBE NO MARKER NEEDED

    mam=CircleMarker( (gps_info['XCoor'],gps_info['YCoor']),'red', 6)
    tkinter_loop.m1.add_marker(mam)
    print("MARKER ADDED ...........")
    #if len(tkinter_loop.m1.markers)>1000:
    #    reduce markers
    print( tkinter_loop.tk_zoomset[ tkinter_loop.tk_zoom], (gps_info['XCoor'] , gps_info['YCoor']) )

    tkinter_loop.tk_image=tkinter_loop.m1.render(zoom=5, center=(14.460648666666668, 50.170264333333336)  )

#    tkinter_loop.tk_image=tkinter_loop.m1.render(zoom=tkinter_loop.tk_zoomset[ tkinter_loop.tk_zoom] , center=(gps_info['XCoor'] , gps_info['YCoor'] )   )
            
    print("make_image_DONE..............")

    
