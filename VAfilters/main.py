from TPTMoogLadder.TPTMoogLadder import *
from TPTSallenKey.TPTSallenKey import *


def plotFrequencyResponse(typeOfFilter, order=2, fc=440, k=3, SR=44100):

    freqs = [440, 880, 1760, 3520, 7040, 14080]

    for f in freqs:

        # Unit impulse signal to get the frequency response of the filter
        t = np.arange(0.5 * (SR//2)) / (SR//2)
        imp = np.zeros(len(t))
        imp[0] = 1

        output = []
        N = len(imp)

        if (typeOfFilter == "MoogLadderLP"):
            TPTMoogLadderLPfilter = TPTMoogLadder(
                fc=f, k=k, filterType="LP", sampleRate=SR)
            for n in range(N):
                output.append(TPTMoogLadderLPfilter.doTPTMoogLadder(imp[n]))

        elif (typeOfFilter == "MoogLadderHP"):
            TPTMoogLadderHPfilter = TPTMoogLadder(
                fc=f, k=k, filterType="HP", sampleRate=SR)
            for n in range(N):
                output.append(TPTMoogLadderHPfilter.doTPTMoogLadder(imp[n]))
        elif (typeOfFilter == "SallenKeyLP"):
            output = SallenKey(imp, filterType='LP',
                               order=2, fc=f, k=k, sampleRate=SR)
            output2 = SallenKey(imp, filterType='LP',
                               order=order, fc=f, k=k, sampleRate=SR)
            
        elif (typeOfFilter == "SallenKeyHP"):
            output = SallenKey(imp, filterType='HP',
                               order=2, fc=f, k=k, sampleRate=SR)
            output2 = SallenKey(imp, filterType='HP',
                               order=order, fc=f, k=k, sampleRate=SR)

        yf = np.abs(scipy.fftpack.fft(output)[:N//2])
        yf2 = np.abs(scipy.fftpack.fft(output2)[:N//2])
        xf = scipy.fft.fftfreq(N, 1 / SR)[:N//2]
        plt.semilogx(xf, 20 * np.log10(abs(yf)), label=f)
        plt.semilogx(xf, 20 * np.log10(abs(yf2)), label=f)
        plt.axvline(f, color='black')  # cutoff frequency

    plt.legend()

    plt.yticks([24, 12, 6, 3, 0, -3, -6, -12, -
               18, -24, -28, -36, -42, -48, -54])
    plt.xlim(0, SR//2)
    plt.ylim(-54, 24)
    plt.grid()
    plt.show()


if __name__ == '__main__':

    plotFrequencyResponse(typeOfFilter="SallenKeyLP", order=1,
                          fc=440, k=0.707, SR=7812)
