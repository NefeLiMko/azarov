import numpy as np
import waveforms.waveform as waves
import os, sys, copy
from scipy.io.wavfile import write, read
from scipy.fftpack import fft, ifft
import numpy as np
import winsound, subprocess
import math

INT16_FAC = (2 ** 15) - 1

INT32_FAC = (2 ** 31) - 1

INT64_FAC = (2 ** 63) - 1

norm_fact = {'int16': INT16_FAC, 'int32': INT32_FAC, 'int64': INT64_FAC, 'float32': 1.0, 'float64': 1.0}

winsound_imported = False


def wavread(filename):
    if (os.path.isfile(filename) == False):
        raise ValueError("Input file is wrong")
    fs, x = read(filename)
    print('fs = ' + str(fs) )
    if (len(x.shape) != 1):
        raise ValueError("Audio file should be mono")

    x = np.float32(x) / norm_fact['float32']
    return fs, x


def wavwrite(y, fs, filename):
    x = copy.deepcopy(y)  # copy array
    x *= INT16_FAC  # scaling floating point -1 to 1 range signal to int16 range
    x = np.int16(x)  # converting to int16 type
    write(filename, fs, x)


def tremolo(n, D, fm, waveform=0, nargout=1):

    if waveform == 1:
        m, n2 = waves.squareWave(D, fm, mode=0)
    elif waveform == 2:
        m, n2 = waves.sawToothWave(D, fm, mode=0, durationN=len(n))
    elif waveform == 3:
        m, n2 = waves.triangleWave(D, fm, mode=0, durationN=len(n))
    else:
        m, n2 = waves.sinusoid(D, fm, durationN=len(n))
    m = m + 1
    result = m * n
    result = result

    if nargout == 1:
        return result

    else:
        return n2, result


fs, x = wavread("aminopen.wav")
ftrem = 1100
D = 0.97
n, out_d1 = tremolo(x, D, ftrem, 0, 0)

wavwrite(out_d1, fs, 'out_d1.wav')
