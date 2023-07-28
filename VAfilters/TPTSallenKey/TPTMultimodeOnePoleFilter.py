import numpy as np


class TPTMultimodeOnePoleFilter:
    def __init__(self, type, sampleRate, fc):

        self.type = type
        self.sampleRate = sampleRate
        self.fc = fc
        wf = np.sqrt(2**(1/8)-1)

        wc = 2*np.pi*fc
        T = 1/sampleRate
        wa = (2/T) * np.tan(wc * T/2)

        self.g = wa * T/2
        self.G = self.g / (1 + self.g)

        self.z1 = 0

    def doFilterStage(self, xn):
        v = (xn - self.z1)*self.G
        lpf = v + self.z1
        self.z1 = v + lpf
        hpf = xn - lpf

        if (self.type == 'LP'):
            return lpf
        elif (self.type == 'HP'):
            return hpf

    def getStorageRegisterValue(self):
        return self.z1

    def getSampleRate(self):
        return self.sampleRate
