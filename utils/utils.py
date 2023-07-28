import matplotlib.pyplot as plt
import scipy
import numpy as np
import librosa
import librosa.display

def plot_impulse_reponse(y, title,SR=44100):
  N = len(y)

  # Calculate the frequency response using the Discrete Fourier Transform (DFT)
  frequency_response = np.abs(scipy.fftpack.fft(y)[:N//2])


  # Frequencies corresponding to the DFT bins

  frequencies = np.fft.fftfreq(N, 1/SR)[:N//2]

  # Plotting the frequency response
  plt.figure(figsize=(20, 10))
  plt.semilogx(frequencies, 20 * np.log10(abs(frequency_response)))
  plt.title('Frequency Response (Magnitude)')
  plt.xlabel('Frequency (Hz)')
  plt.ylabel('Magnitude (dB)')
  plt.xlim(1, SR//2)
  plt.grid(True, which="both", ls="-")

  plt.ylim(-54, 24)
  plt.tight_layout()
  plt.savefig(title)

def plot_spectrogram(y, title, SR=44100):

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=2048)), ref=np.max)

    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    img = librosa.display.specshow(D, y_axis='linear', x_axis='time', sr=SR, ax=ax, n_fft=2048)
    ax.set(title='Linear-frequency power spectrogram')
    ax.label_outer()
    plt.savefig(title)

def plot_wave(y, title, SR=44100):
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    librosa.display.waveshow(y, sr=SR, ax=ax)
    ax.set(title='waveform')
    ax.label_outer()
    plt.savefig(title)