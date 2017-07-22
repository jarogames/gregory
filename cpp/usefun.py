#!/usr/bin/python3
import ctypes
import threading
import time
'''
Start   C   function from .so   in thread
'''
_sum = ctypes.CDLL('libFunq.so')
_sum.fso.argtypes = ()
#_sum.our_function.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int))

def our_function(numbers):
    global _sum
    num_numbers = len(numbers)
    array_type = ctypes.c_int * num_numbers
    result = _sum.our_function(ctypes.c_int(num_numbers), array_type(*numbers))
    return int(result)

def tfso():
    time.sleep(2)
    r=_sum.fso()
    return r

t=threading.Thread( target=tfso )
#t.setDaemon(True)
t.start()
print('ending',_sum.fso())
