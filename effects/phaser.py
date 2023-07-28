import numpy as np
from .lfo import LFO
import math

def phaser(x, fc, Wb, mod_freq, mod_amp):

    xh = [0, 0]
    y = np.zeros_like(x)

    lfo = LFO(44100, mod_freq, mod_amp, offset=-mod_amp/2)

    Wc = 2 * fc / 44100

    for n in range(len(x)):

        c = (np.tan(np.pi * Wb / 2) - 1) / (np.tan(np.pi * Wb / 2) + 1)
        d = -np.cos(np.pi * Wc)

        xh_new = x[n] - d * (1 - c) * xh[0] + c * xh[1]
        ap_y = -c * xh_new + d * (1 - c) * xh[0] + xh[1]
        xh = [xh_new, xh[0]]
        y[n] = 0.5 * (x[n] + ap_y)  # change to plus for bandreject

        Wc = 2 * (fc + lfo.tick()) / 44100

    return y
