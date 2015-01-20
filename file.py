#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *
from scipy.io import wavfile
import os
import pdb

signal = 0
filename = 0
answer = 0
w = 0
p = 3
k = m = 0
lowpass = 201/p
highpass = 27000/p

def test():
    if "K" in filename:
        a = "K"
    elif "M" in filename:
        a = "M"

    if answer == a:
        return 0
    else:
        return 1

def readF():
#    pdb.set_trace()
    global signal, sampleRate, k, m, answer
#    signal = fromfile(filename, 'int16')[:44]   

    sampleRate, signal = wavfile.read(filename, True)
    channels = len(signal.shape)

    if channels > 1:
        signal = signal[:, 0]

    frameWidthT = 300 # (ms)
    framesPerSec = 1000/frameWidthT
    frameWidthS = sampleRate/framesPerSec
    n = int(len(signal)/frameWidthS)

    for i in range(n-1):
        frame = signal[i*frameWidthS:(i+1)*frameWidthS]
        frame = rfft(frame)
        print len(frame)
        frame = frame[:int(len(frame)/2)]
        frame = abs(frame)
        frame = frame[::p]

        draw(1, frame)
        x = frame[85:225].argmax()
        if abs(x - 125) < abs(x - 210):
            m += 1
        else:
            k += 1


    foo() 
#    draw(0, signal)

#    m, k = f0()
    if m > k:
        answer = "M"
    else:
        answer = "K"
    r = test()
    print filename + " : " + ("OK" if r == 0 else "WRONG")
    return r 

def foo():
    global signal
    signal = rfft(signal) 
    desc()
    length = int(len(signal)/2)
    signal = signal[:length]
    signal = abs(signal) 
    signal = signal[::p]
    signal[:lowpass] = 0
    signal = signal[:highpass]
    signal = signal/signal.max()
 

def desc():
    print sampleRate
    print "Hz : " + str(signal.argmax())
    print "A : " + str(signal.max())
    freq = fftfreq(len(signal)) 
    print "len(signal) : " + str(len(signal))
    print "len(freq) : " + str(len(freq))

def draw(b, sig):
    xlim([0,highpass])
    xlim([0,1000])
    plot(sig)
    savefig(filename + '.pdf')
    if b == 1:
        show()

def f5():
    global m, k
    for i in range(30):
        m += sum(signal[85*i:185*i])
        k += sum(signal[165*i:225*i])
    return (m, k)
    

def f4():
    x = signal.argmax()
    if abs(x - 125) < abs(x - 210):
        m = 1;
        k = 0;
    else:
        m = 0;
        k = 1;
    return (m, k)

def f3():
    if signal.argmax() > 130:
        k = 1
        m = 0
    else:
        k = 0
        m = 1
    return (m, k)
    
def f2():
    for x in signal[50:100]:
        if x > 0.40:
            k = 0
            m = 1
        else:
            k = 1
            m = 0
    return (m, k)
    
def f1():
    m = sum(signal[85:180])
    k = sum(signal[165:255])
    return (m, k)

def f0():
    return (0, 0)

if __name__ == "__main__":
    set_printoptions(threshold='nan')
    if len(sys.argv) <= 1:
        print "Usage: " + sys.argv[0] + " [filename.wav]"
    else:
        filename = sys.argv[1]
        r = readF()
        sys.exit(r) 

#    dir = "train/"
#    for file in os.listdir(dir):
#        if file.endswith('.wav'):
#            print file
#            read(dir+file)
