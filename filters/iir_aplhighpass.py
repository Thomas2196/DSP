import numpy as np

def iir_aphighpass(x, Wc):
    # Wc is the normalized cut-off frequency 0<Wc<1, i.e. 2*fc/fS
    c = (np.tan(np.pi * Wc / 2) - 1) / (np.tan(np.pi * Wc / 2) + 1)
    xh = 0
    y = np.zeros_like(x)
    
    for n in range(len(x)):
        xh_new = x[n] - c * xh
        ap_y = c * xh_new + xh
        xh = xh_new
        y[n] = 0.5 * (x[n] - ap_y)

    return y