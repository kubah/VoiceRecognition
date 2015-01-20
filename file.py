#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *
from scipy.io import wavfile
import os
import pdb

k = m = 0
frame = 0
a = 0
lowpass = 50
highpass = 400

def readF(filename):
    global k, m, p, a, frame
    r = 0
#    pdb.set_trace()

    sampleRate, signal = wavfile.read(filename)
    channels = len(signal.shape)

    if channels > 1:
        signal = signal[:, 0]

    frameWidthT = 1000 # (ms)
    framesPerSec = 1000/frameWidthT
    frameWidthS = sampleRate/framesPerSec
    n = int(len(signal)/frameWidthS)
    
    a = 1./framesPerSec
    
    """
    print "sampleRate = " + str(sampleRate)
    print "len(signal) = " + str(len(signal))
    print "framesPerSec = " + str(framesPerSec)
    print "frameWidthS = " + str(frameWidthS)
    print "n = " + str(n)
    """

    p = 0.9
    for i, j in zip(frange(0, n-1, p), frange(1, n, p)):
        frame = signal[i*frameWidthS:j*frameWidthS]
        frame = rfft(frame)
        frame = abs(frame)
        frame = frame[:highpass*a]
        frame[:lowpass*a] = 0
        frame = frame/frame.max()

        if frame[80*a:120*a].max() > 0.3:
            r = 1;

        x, y = f2()     
#        x, y = f1()
#        x, y = f0()

        m += x
        k += y
        
        print m, k

    if m == k:
        if r == 1:
            m += 1
        else:
            k += 1
                
#        xlim([lowpass*a,highpass*a])
#        plot(frame)

#    directory, filename = os.path.split(filename)
#    savefig('./pdf/' + filename + '.pdf')
#    show()

    if m > k:
        print "M"
    elif m < k:
        print "K"
    else:
        print "S"

def f2():
    w = 100
    f, s = 80, 150
    m = k = 0
    m += sum(frame[f*a:(f+w)*a])
    k += sum(frame[s*a:(s+w)*a])
#    """ 
    if m > k*0.55:
        m, k = 1, 0 
    else:
        m, k = 0, 1
#    """
    return (m, k)

def f1():
    m = k = 0
    x = frame[70*a:170*a].max()
    y = frame[170*a:270*a].max()
    if x > y:
        m, k = 1, 0 
    else:
        m, k = 0, 1
    return (m, k)

def f0():
    m = k = 0
    m += sum(frame[85*a:180*a]) # 85 180 -- 50ms
    k += sum(frame[165*a:255*a]) # 165 255 -- 50ms
    if m > k:
        m, k = 1, 0
    else:
        m, k = 0, 1
    return (m, k)
    

if __name__ == "__main__":
    set_printoptions(threshold='nan')
    if len(sys.argv) <= 1:
        print "Usage: " + sys.argv[0] + " [filename.wav]"
    else:
        readF(sys.argv[1])
