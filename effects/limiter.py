def limiter(x, lt):
    # Initialize parameters
    at = 0.3
    rt = 0.01
    delay = 5
    xpeak = 0
    g = 1
    buffer = [0] * delay

    y = [0] * len(x)

    for n in range(len(x)):
        a = abs(x[n])
        if a > xpeak:
            coeff = at
        else:
            coeff = rt

        xpeak = (1 - coeff) * xpeak + coeff * a
        f = min(1, lt / xpeak)

        if f < g:
            coeff = at
        else:
            coeff = rt

        g = (1 - coeff) * g + coeff * f
        y[n] = g * buffer[-1]
        buffer = [x[n]] + buffer[:-1]

    return y
