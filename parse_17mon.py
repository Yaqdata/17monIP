#!/usr/bin/python
#!-*- coding:utf-8 -*-
import sys

PY2 = True

#import functools
import os
import socket
import struct

_unpack_V = lambda b: struct.unpack("<L", b)
_unpack_N = lambda b: struct.unpack(">L", b)
_unpack_C = lambda b: struct.unpack("B", b)

fp =  open(os.path.join(os.path.dirname(__file__), "17monipdb.dat"), "rb")

dat = fp.read()
offset, = _unpack_N(dat[:4])
index = dat[4:offset]
#def memoize(func):
#    """Memoize for functions based on memory
#    """
#    cache = func.cache = {}
#
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        key = "{0}{1}".format(args, kwargs)
#        if key not in cache:
#            cache[key] = func(*args, **kwargs)
#        return cache[key]
#    return wrapper
#

#@memoize
def _find_ip(ip):
    nip = socket.inet_aton(ip)
    #print "nip:%s"%( _unpack_N(nip))
    tmp_offset = int(ip.split(".")[0]) * 4
    #print "tmp_offset:%s" % tmp_offset
    start, = _unpack_V(index[tmp_offset:tmp_offset + 4])
    index_offset = index_length = 0
    max_comp_len = offset - 1028

    start = start * 8 + 1024
    start_nip = 16777216
    while start < max_comp_len:
        #if index[start:start + 4] >= nip:
            index_offset, = _unpack_V(index[start + 4:start + 7] + chr(0).encode("utf-8"))
            end_nip,   =   _unpack_N(index[start :start + 4])
            #print "start=%s index_offset=%s" % (start, index_offset)
            if PY2:
                index_length, = _unpack_C(index[start + 7])
            else:
                index_length = index[start + 7]
            start += 8
            res_offset = offset + index_offset - 1024
            print start_nip,  end_nip, dat[res_offset:res_offset + index_length]
            start_nip = end_nip + 1
   


def find(ip):
    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        return

    return _find_ip(ip)
print find('1.0.0.0')
                                                 
