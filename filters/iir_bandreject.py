import numpy as np

def iir_apbandreject(x, Wc, Wb):


    c = (np.tan(np.pi * Wb / 2) - 1) / (np.tan(np.pi * Wb / 2) + 1)
    d = -np.cos(np.pi * Wc)
    xh = [0, 0]
    y = np.zeros_like(x)
    
    for n in range(len(x)):
        xh_new = x[n] - d * (1 - c) * xh[0] + c * xh[1]
        ap_y = -c * xh_new + d * (1 - c) * xh[0] + xh[1]
        xh = [xh_new, xh[0]]
        y[n] = 0.5 * (x[n] + ap_y)  # change to plus for bandreject

    return y