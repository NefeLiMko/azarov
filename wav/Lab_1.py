import numpy as np
import matplotlib
import wave
import struct


wavNum = 0
frame = [[], []]
framerate = 1024
waveFile = wave.open('speech_phone_number.wav', 'r')
length = waveFile.getnframes()
print(length // 1024)
for i in range(0, length):
    wavNum += 1
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)
    if wavNum <= 1024:
        frame[i // 1024].append(int(data[0]))
    else:
        wavNum = 0
        frame.append([])
        frame[i // 1024].append(int(data[0]))
