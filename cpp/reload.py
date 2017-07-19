#!/usr/bin/python3
import ctypes
import threading
import time
'''
Start   C   function from .so   in thread
try to reload   .so
'''
#----- this is to reload ----
libdl = ctypes.CDLL("libdl.so")
libdl.dlclose.argtypes = [ctypes.c_void_p]

#_sum = ctypes.CDLL('libFunq.so')
_sum = ctypes.PyDLL('libFunq.so')
_sum.fso.argtypes = ()
#_sum.our_function.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int))

def tfso():
    time.sleep(0.2)
    r=_sum.fso()
    return r

t=threading.Thread( target=tfso )
#t.setDaemon(True)
t.start()
print('ending',_sum.fso())
############### readline
import fileinput
i=0
for line in fileinput.input():
    i=i+1
    print("> ",line.rstrip())
    if line.rstrip()=='re':
        #======= REMOVE 
        libdl.dlclose(_sum._handle)
        del _sum
        #======= RELOAD
        _sum = ctypes.CDLL('libFunq.so')
        _sum.fso.argtypes = (ctypes.c_int,)
    print('after reload',_sum.fso(ctypes.c_int(i)))
    if line.rstrip()=='q':quit()
    pass
