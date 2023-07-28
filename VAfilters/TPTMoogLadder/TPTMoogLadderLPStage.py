import numpy as np


class TPTMoogLadderLPStage:
    def __init__(self, sampleRate, fc):

        self.sampleRate = sampleRate
        self.fc = fc

        wc = 2*np.pi*fc
        T = 1/sampleRate
        wa = (2/T) * np.tan(wc * T/2)

        g = wa*T/2
        self.G = g / (1 + g)

        self.z1 = 0

    def doFilterStage(self, xn):
        v = (xn - self.z1)*self.G
        y = v + self.z1
        self.z1 = y + v
        return y

    def getStorageRegisterValue(self):
        return self.z1

    def getSampleRate(self):
        return self.sampleRate
