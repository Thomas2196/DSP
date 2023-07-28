import numpy as np

def unicomb(x, BL, FB, FF, M):
  N = len(x)

  Delayline = np.zeros(M)  # memory allocation for length 10
  y = np.zeros(N)  # result array

  for n in range(N):
      xh = x[n] + FB * Delayline[M-1]
      y[n] = FF * Delayline[M-1] + BL * xh
      Delayline = np.concatenate(([x[n]], Delayline[0:M-1]))
  
  return y

