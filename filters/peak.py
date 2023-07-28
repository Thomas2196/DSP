import numpy as np

def peak(x, Wc, Wb, G):
    V0 = 10 ** (G / 20)
    H0 = V0 - 1
    
    if G >= 0:
        c = (np.tan(np.pi * Wb / 2) - 1) / (np.tan(np.pi * Wb / 2) + 1)  # boost
    else:
        c = (np.tan(np.pi * Wb / 2) - V0) / (np.tan(np.pi * Wb / 2) + V0)  # cut
        
    d = -np.cos(np.pi * Wc)
    xh = [0, 0]
    y = np.zeros_like(x)
    
    for n in range(len(x)):
        xh_new = x[n] - d * (1 - c) * xh[0] + c * xh[1]
        ap_y = -c * xh_new + d * (1 - c) * xh[0] + xh[1]
        xh = [xh_new, xh[0]]
        y[n] = 0.5 * H0 * (x[n] - ap_y) + x[n]

    return y

