import os, sys, copy
from scipy.io.wavfile import write, read
from scipy.fftpack import fft, ifft
import numpy as np


INT16_FAC = (2 ** 15) - 1

INT32_FAC = (2 ** 31) - 1

INT64_FAC = (2 ** 63) - 1

norm_fact = {'int16': INT16_FAC, 'int32': INT32_FAC, 'int64': INT64_FAC, 'float32': 1.0, 'float64': 1.0}

winsound_imported = False


def wavread(filename):
    if (os.path.isfile(filename) == False):
        raise ValueError("Input file is wrong")
    fs, x = read(filename)
    print('fs = ' + str(fs))
    if (len(x.shape) != 1):
        raise ValueError("Audio file should be mono")

    x = np.float32(x) / norm_fact['float32']
    return fs, x


def wavwrite(y, fs, filename):
    x = copy.deepcopy(y)  # copy array
    x *= INT16_FAC  # scaling floating point -1 to 1 range signal to int16 range
    x = np.int16(x)  # converting to int16 type
    write(filename, fs, x)


def echo(filename,  fb=15):
    fs, x = wavread(filename)
    time_delay = int(fs / 10 * 6)
    dry = 0.95
    wet = 0.05
    print(len(x), time_delay)
    inp = x.tolist()
    for i in range(time_delay):
        inp.append(0)
    x = copy.deepcopy(inp)
    print(len(x))
    y = []

    for id in range(len(x)):
        if id<time_delay:
            y.append(dry * x[id])
        else:
            #y.append(x[id-time_delay] + fb*y[id-time_delay])
            y.append(dry * x[id] + wet*(x[id-time_delay] + fb*y[id-time_delay]))
    return fs, y/np.max(y)



fs, out = echo("wav/aminopen.wav")
print(len(out))
wavwrite(out, fs, "out.wav")