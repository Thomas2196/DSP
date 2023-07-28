import numpy as np
import scipy.signal as signal
from scipy.fft import fft, fftfreq
import scipy.fftpack
import matplotlib.pyplot as plt

from TPTMoogLadder.TPTMoogLadderLPStage import *
from TPTMoogLadder.TPTMoogLadderHPStage import *


class TPTMoogLadder:
    def __init__(self, filterType, fc, k, sampleRate):
        self.filterType = filterType
        self.fc = fc
        self.k = k
        self.sampleRate = sampleRate

        if (filterType == "HP"):
            self.filter1 = TPTMoogLadderHPStage(sampleRate=sampleRate, fc=fc)
            self.filter2 = TPTMoogLadderHPStage(sampleRate=sampleRate, fc=fc)
            self.filter3 = TPTMoogLadderHPStage(sampleRate=sampleRate, fc=fc)
            self.filter4 = TPTMoogLadderHPStage(sampleRate=sampleRate, fc=fc)

        elif (filterType == "LP"):

            self.filter1 = TPTMoogLadderLPStage(sampleRate=sampleRate, fc=fc)
            self.filter2 = TPTMoogLadderLPStage(sampleRate=sampleRate, fc=fc)
            self.filter3 = TPTMoogLadderLPStage(sampleRate=sampleRate, fc=fc)
            self.filter4 = TPTMoogLadderLPStage(sampleRate=sampleRate, fc=fc)

    def doTPTMoogLadder(self, xn):

        # Cutoff pre-warping
        wc = 2*np.pi*self.fc
        T = 1/self.sampleRate
        wa = np.tan(wc * T/2)

        s1 = self.filter1.getStorageRegisterValue()
        s2 = self.filter2.getStorageRegisterValue()
        s3 = self.filter3.getStorageRegisterValue()
        s4 = self.filter4.getStorageRegisterValue()

        if (self.filterType == "HP"):

            g = 1 / (1 + wa)  # Instantaneous gain

            # y = G*eps+S
            G = g*g*g*g
            S = -(g*g*g*g) * s1 - (g*g*g) * s2 - \
                (g*g) * s3 - g * s4

        elif (self.filterType == "LP"):
            g = wa / (1 + wa)  # Instantaneous gain

            # y = G*eps+S
            G = g*g*g*g
            S = g*g*g*(s1 * (1-g)) + g*g*(s2 * (1-g)) + \
                g*(s3 * (1-g)) + (s4 * (1-g))

        u = (xn - self.k*S) / (1 + self.k*G)

        filterOut = self.filter4.doFilterStage(self.filter3.doFilterStage(
            self.filter2.doFilterStage(self.filter1.doFilterStage(u))))

        return filterOut
