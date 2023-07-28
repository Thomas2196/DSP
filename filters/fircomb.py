import numpy as np

def fircomb(x, g, delay):
  N = len(x)

  Delayline = np.zeros(delay)  # memory allocation for length 10
  y = np.zeros(N)  # result array

  for n in range(N):
      y[n] = x[n] + g * Delayline[delay-1]
      Delayline = np.concatenate(([x[n]], Delayline[:delay-1]))
  
  return y

