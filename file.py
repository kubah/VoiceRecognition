#!/usr/bin/env python
# -*- coding: utf -*-
from pylab import *
from scipy.io import wavfile
import os
import warnings

warnings.filterwarnings('ignore')
k = m = 0
frame = 0
a = 0
lowpass = 50
highpass = 400

def readF(filename):
    global k, m, p, a, frame
    r = 0

    sampleRate, signal = wavfile.read(filename)
    channels = len(signal.shape)

    if channels > 1:
        signal = signal[:, 0]

    frameWidthT = 600 # (ms)
    framesPerSec = 1000/frameWidthT
    frameWidthS = sampleRate/framesPerSec
    n = int(len(signal)/frameWidthS)
    
    a = 1./framesPerSec
    p = 0.9

    for i, j in zip(frange(0, n-1, p), frange(1, n, p)):
        frame = signal[i*frameWidthS:j*frameWidthS]
        frame = rfft(frame)
        frame = frame[:highpass*a]
        frame = abs(frame)
        frame = frame/frame.max()

        if frame[80*a:120*a].max() > 0.3:
            r = 1;

        x, y = f()     
        m += x
        k += y
        
    if m == k:
        if r == 1:
            m += 1
        else:
            k += 1
    if m > k:
        print "M"
    else:
        print "K"

def f():
    w = 100
    f, s = 80, 150
    m = k = 0
    m += sum(frame[f*a:(f+w)*a])
    k += sum(frame[s*a:(s+w)*a])
    if m > k*0.55:
        m, k = 1, 0 
    else:
        m, k = 0, 1
    return (m, k)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Usage: " + sys.argv[0] + " [filename.wav]"
    else:
        readF(sys.argv[1])
