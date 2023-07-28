import numpy as np

def fft(x):
    
    n = len(x)

    if N <= 1: return x

    try:
      if N%2 !=0: raise ValueError 
    except ValueError:
      print("Error: radix 2 Cooley-Tukey not respected")

    even = []
    for k in range(0, n/2):
      even.append(x[2*k])
    evenFFT = fft(even)

    odd =  []
    for k in range(0, n/2):
          odd.append(x[2*k+1])
    oddFFT = fft(odd)

    y = np.zeros(n)
    for k in range(0, n/2):
      kth = -2 * k * np.pi / n
      wk = np.cos(kth) + np.sin(kth) * 1j
      y[k] = evenFFT[k] + wk * oddFFT[k]
      y[k + n/2] = evenFFT[k] - wk * oddFFT[k]
