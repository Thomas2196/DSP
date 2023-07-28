import numpy as np

def highshelving(x, Wc, G):
    V0 = 10 ** (G / 20)
    H0 = V0 - 1
    
    if G >= 0:
        c = (np.tan(np.pi * Wc / 2) - 1) / (np.tan(np.pi * Wc / 2) + 1)  # boost
    else:
        c = (np.tan(np.pi * Wc / 2) - V0) / (np.tan(np.pi * Wc / 2) + V0)  # cut
        
    xh = 0
    y = np.zeros_like(x)
    
    for n in range(len(x)):
        xh_new = x[n] - c * xh
        ap_y = c * xh_new + xh
        xh = xh_new
        y[n] = 0.5 * H0 * (x[n] - ap_y) + x[n]

    return y

