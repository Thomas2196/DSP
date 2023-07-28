import numpy as np
import math

from .delay import Delay
from.lfo import LFO


def vibrato(x, SR, mod_freq, mod_width):

    delay = mod_width  # basic delay of input sample in sec
    avg_delay = round(delay * SR)  # basic delay in # samples
    width = math.floor(SR * mod_width)
    if width > avg_delay:
        raise ValueError('delay greater than basic delay !!!')

    max_delay = avg_delay + width * 2 + 3  # length of the entire delay
    delay_line = np.zeros(max_delay)  # memory allocation for delay
    y = np.zeros_like(x)  # memory allocation for output vector

    lfo = LFO(44100, mod_freq, width)

    for n in range(len(x)):
        tap = avg_delay + lfo.tick()
        i = int(np.floor(tap))
        frac = tap - i

        delay_line = np.concatenate(([x[n]], delay_line[:-1]))

        # Linear Interpolation
        y[n] = delay_line[i + 1] * frac + delay_line[i] * (1 - frac)

        # Allpass Interpolation
        # y[n] = (delay_line[i + 1] + (1 - frac) * delay_line[i] - (1 - frac) * ya_alt)
        # ya_alt = y[n]

        # Spline Interpolation
        # y[n] = delay_line[i + 1] * frac**3 / 6 + delay_line[i] * ((1 + frac)**3 - 4 * frac**3) / 6 + delay_line[i - 1] * ((2 - frac)**3 - 4 * (1 - frac)**3) / 6 + delay_line[i - 2] * (1 - frac)**3 / 6

    return y

'''                                                      
    x ----------->[ delay 1 ]---------> y
                      /|\                                  
                       |                                   
                    [ LFO ]                                                                                
'''
class Vibrato():
    def __init__(self, sample_rate, delay, mod_width, mod_freq):
        self.sample_rate = sample_rate
        self.avg_delay = math.floor(sample_rate * delay)
        width = math.floor(sample_rate * mod_width)
        if self.avg_delay < width:
            self.avg_delay = width
        max_delay = self.avg_delay + 2 * width + 3
        self.delay_line = Delay(max_delay)
        self.lfo = LFO(sample_rate, mod_freq, width)
        return

    def process(self, x):
        tap = self.avg_delay + self.lfo.tick()
        i = math.floor(tap)

        # Linear Interpolation 
        frac = tap - i
        candidate1 = self.delay_line.go_back(i)
        candidate2 = self.delay_line.go_back(i + 1)
        interp = frac * candidate2 + (1 - frac) * candidate1

        self.delay_line.push(x)
        return interp