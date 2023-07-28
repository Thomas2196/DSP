import numpy as np
import math
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sd

from filters.iir_aplowpass import iir_aplowpass
from filters.iir_aplhighpass import iir_aphighpass
from filters.iir_apbandpass import iir_apbandpass
from filters.iir_bandreject import iir_apbandreject
from filters.lowshelving import lowshelving
from filters.highshelving import highshelving
from filters.peak import peak
from filters.unicomb import unicomb
from filters.fircomb import fircomb
from filters.iircomb import iircomb

from effects.wahwah import wahwah
from effects.phaser import phaser
from effects.vibrato import vibrato, Vibrato
from effects.echo import echo, Echo
from effects.flanger import Flanger
from effects.chorus import Chorus

from effects.limiter import limiter

from utils.utils import plot_impulse_reponse, plot_spectrogram, plot_wave

SR = 44100

t = np.arange(0.5 * (SR//2)) / (SR//2)
x = np.zeros(len(t))
x[0] = 1  # unit impulse signal of length 100


def test_iir_aplowpass():
    fc = 0.1*SR
    Wc = 2 * fc / SR
    y = iir_aplowpass(x, Wc)
    plot_impulse_reponse(y, './results/allpass_LP.png')


def test_iir_aphighpass():
    fc = 0.1*SR
    Wc = 2 * fc / SR
    y = iir_aphighpass(x, Wc)
    plot_impulse_reponse(y, './results/allpass_HP.png')


def test_iir_apbandpass():
    fc = 0.1*SR
    fb = 0.022 * SR
    Wc = 2 * fc / SR
    Wb = 2 * fb / SR
    y = iir_apbandpass(x, Wc, Wb)
    plot_impulse_reponse(y, './results/allpass_BP.png')


def test_iir_apbandreject():
    fc = 0.1*SR
    fb = 0.022 * SR
    Wc = 2 * fc / SR
    Wb = 2 * fb / SR
    y = iir_apbandreject(x, Wc, Wb)
    plot_impulse_reponse(y, './results/allpass_BR.png')


def test_lowshelving():
    fc = 1000
    Wc = 2 * fc / SR
    G = 15
    y = lowshelving(x, Wc, G)
    plot_impulse_reponse(y, './results/shelving_LP.png')


def test_highshelving():
    fc = 1000
    Wc = 2 * fc / SR
    G = 15
    y = highshelving(x, Wc, G)
    plot_impulse_reponse(y, './results/shelving_HP.png')


def test_peak():
    fc = 0.1*SR
    fb = 0.022 * SR
    Wc = 2 * fc / SR
    Wb = 2 * fb / SR
    G = -15
    y = peak(x, Wc, Wb, G)
    plot_impulse_reponse(y, './results/peak.png')


def test_fircomb():
    g = 0.5  # feedback
    delay = 6
    y = fircomb(x, g, delay)
    plot_impulse_reponse(y, './results/fir_comb.png')


def test_iircomb():
    g = 0.5  # feedback
    c = 1  # scaling factor
    delay = 6
    y = iircomb(x, g, c, delay)
    plot_impulse_reponse(y, './results/iir_comb.png')


def test_unicomb():
    BL = 0.5  # blend parameter
    FB = -0.5  # feedback parameter
    FF = 1  # feedforward parameter
    M = 6  # delay memory size
    y = unicomb(x, BL, FB, FF, M)
    plot_impulse_reponse(y, './results/universal_comb.png')


def test_wah_wah():
    mean = 0
    std = 1
    x = np.random.normal(mean, std, size=60*len(t))

    fc = 5000
    fb = 10
    Wc = 2 * fc / SR
    Wb = 2 * fb / SR
    mod_amp = 1000
    mod_freq = 2

    y = wahwah(x, fc, Wb, mod_freq, mod_amp)

    plot_spectrogram(y, './results/wahwah.png')


def test_phaser():
    mean = 0
    std = 1
    x = np.random.normal(mean, std, size=60*len(t))

    n = 4
    fc = 1000
    fb = 0.022 * SR
    Wc = 2 * fc / SR
    Wb = 2 * fb / SR

    mod_amp = 1000
    mod_freq = 2

    y = phaser(x, fc, Wb, mod_freq, mod_amp)
    # for i in range(n-1):
    #     fc=2*fc
    #     y = phaser(y, fc, Wb, mod_freq, mod_amp)

    plot_spectrogram(y, './results/phaser.png')


def test_vibrato():
    t = np.arange(1 * SR) / SR
    x = np.sin(2*np.pi*t*1000)

    width = 0.008
    mod_freq = 2

    y = vibrato(x, SR, mod_freq, width)

    plot_wave(y, './results/vibrato.png')

    y = y / max(np.abs(y))
    sd.write('./results/vibrato.wav', y, SR)

def test_vibrato_2():
    t = np.arange(1 * SR) / SR
    x = np.sin(2*np.pi*t*1000)
    y = np.zeros(len(x))

    delay = 0.008
    mod_width = 0.004
    mod_freq = 2.3
    vibrato = Vibrato(SR, delay, mod_width, mod_freq)
    # Start Processing
    for i in range(len(x)):
        y[i] = vibrato.process(x[i])

    output_file = "./results/vibrato.wav"
    y = y / max(np.abs(y))
    sd.write(output_file, y, SR)

def test_echo():
    x, sr = librosa.load('./rythm.wav', sr=SR)

    echo_gains = [0.3, 0.25, 0.125, 0.0625, 0.03125, 0.015625]
    echo_delays = [0.10, 0.20, 0.30, 0.40, 0.50]

    y = echo(x, 44100, echo_delays, echo_gains)

    plot_wave(y, './results/echo.png')

    y = y / max(np.abs(y))
    sd.write('./results/echo.wav', y, SR)

def test_echo_2():
    x, fs  = sd.read('./rythm.wav')
    y = np.zeros(len(x))

    echo_gains = [0.5]
    echo_delays = [0.05]
    echo = Echo(fs, echo_delays, echo_gains, 0.5)
    # Start Processing
    for i in range(len(x)):
        y[i] = echo.process(x[i])

    output_file = "./results/echo.wav"
    y = y / max(np.abs(y))
    sd.write(output_file, y, fs)

def test_flanger():
    x, _  = sd.read('./input.wav')
    y = np.zeros(len(x))

    delay = 0.01
    mod_width = 0.003
    mod_freq = 1
    flanger = Flanger(SR, delay, mod_width, mod_freq)

    # Start Processing
    for i in range(len(x)):
        y[i] = flanger.process(x[i])

    plot_spectrogram(y, './results/flanger.png')

    output_file = "./results/flanger.wav"
    y = y / max(np.abs(y))
    sd.write(output_file, y, SR)

def test_chorus():
    x, fs  = sd.read('./input.wav')
    y = np.zeros(len(x))

    gains = [0.5]
    delays = [0.05]
    mod_widths = [0.005]
    mod_freqs = [2]
    dry_gain = 1
    chorus = Chorus(fs, delays, mod_freqs, mod_widths, gains, dry_gain)
    
    # Start Processing
    for i in range(len(x)):
        y[i] = chorus.process(x[i])

    plot_spectrogram(y, './results/chorus.png')

    output_file = "./results/chorus.wav"
    y = y / max(np.abs(y))
    sd.write(output_file, y, fs)

def test_limiter()

if __name__ == '__main__':
    # test_iir_aplowpass()
    # test_iir_aphighpass()
    # test_iir_apbandpass()
    # test_iir_apbandreject()
    # test_lowshelving()
    # test_highshelving()
    # test_peak()
    # test_fircomb()
    # test_iircomb()
    # test_unicomb()

    # test_wah_wah()
    # test_phaser()
    # test_vibrato_2()
    # test_echo_2()
    # test_flanger()
    test_chorus()