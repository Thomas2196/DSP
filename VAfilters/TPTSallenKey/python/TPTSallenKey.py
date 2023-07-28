
import numpy as np
import scipy.signal as signal
from scipy.fft import fft, fftfreq
import scipy.fftpack
import matplotlib.pyplot as plt

from TPTSallenKey.TPTSallenKeyLPStage import *
from TPTSallenKey.TPTSallenKeyHPStage import *
from TPTSallenKey.TPTMultimodeOnePoleFilter import *

def SallenKey(signal, filterType, order, fc, k, sampleRate):
    # TODO Generalized ladder to correct the cutoff frequency at higher order
    
    N = len(signal)
    output= []
    order=order//2

    TPTSallenKeyfilter = TPTSallenKey(
                fc=fc, k=k, filterType=filterType, sampleRate=sampleRate)
    for n in range(N):
        output.append(TPTSallenKeyfilter.doTPTSallenKey(signal[n]))

    if(order>1):
        for o in range(order-1):
            TPTSallenKeyfilter = TPTSallenKey(
                    fc=fc, k=k, filterType=filterType, sampleRate=sampleRate)
            for n in range(N):
                output[n] = TPTSallenKeyfilter.doTPTSallenKey(output[n])

        
    return output


class TPTSallenKey:
    def __init__(self, filterType, fc, k, sampleRate):
        self.filterType = filterType
        self.fc = fc
        self.k = k
        self.sampleRate = sampleRate

        if (filterType == "HP"):
            self.HPF1 = TPTMultimodeOnePoleFilter(
                type='HP', sampleRate=sampleRate, fc=fc)
            self.LPF1 = TPTMultimodeOnePoleFilter(
                type='LP', sampleRate=sampleRate, fc=fc)
            self.HPF3 = TPTMultimodeOnePoleFilter(
                type='HP', sampleRate=sampleRate, fc=fc)

        elif (filterType == "LP"):            
            self.LPF1 = TPTMultimodeOnePoleFilter(
                type='LP', sampleRate=sampleRate, fc=fc)
            self.LPF2 = TPTMultimodeOnePoleFilter(
                type='LP', sampleRate=sampleRate, fc=fc)
            self.HPF1 = TPTMultimodeOnePoleFilter(
                type='HP', sampleRate=sampleRate, fc=fc)
    

    def doTPTSallenKey(self, xn):
        # Cutoff pre-warping
        wc = 2*np.pi*self.fc
        T = 1/self.sampleRate
        wa = (2/T) * np.tan(wc * T/2)

        g = wa*(T/2)  # Instantaneous gain
        G = g/(1.0 + g) # Feedworward coeff

        if (self.filterType == "HP"):
            s1 = self.HPF1.getStorageRegisterValue()
            s2 = self.LPF1.getStorageRegisterValue()
            s3 = self.HPF3.getStorageRegisterValue()
            
            beta_3 = -G/(1.0 + g)
            beta_2 = 1.0/(1.0 + g)

            G35 = 1.0/(1.0 - self.k*G + self.k*G*G)
           
            y1 = self.HPF1.doFilterStage(xn)

            S35H = s3*beta_3 + s2*beta_2

            u = G35 * (y1 + S35H)

            y = self.k * u

            self.LPF1.doFilterStage(self.HPF3.doFilterStage(y))

            if (self.k > 0): y *= 1/self.k

        
        elif (self.filterType == "LP"):
            s1 = self.LPF1.getStorageRegisterValue()
            s2 = self.LPF2.getStorageRegisterValue()
            s3 = self.HPF1.getStorageRegisterValue()
            
            beta_2 = (self.k-self.k*G)/(1+g)
            beta_3 = -1.0/(1.0+g)

            alpha = 1.0/(1.0 - self.k*G + self.k*G*G)

            y1 = self.LPF1.doFilterStage(xn)
            S35 = s3*beta_3 + s2*beta_2 # Feedback value

            u = alpha * (y1 + S35)

            y = self.k * self.LPF2.doFilterStage(u)

            self.HPF1.doFilterStage(y)

            if (self.k > 0): y *= 1/self.k

            return  y



        return y
