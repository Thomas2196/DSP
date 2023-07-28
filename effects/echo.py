import numpy as np
from .delay import Delay
'''      
                                                              ___
    x -----+-----------------------------------gain in------>|   |
           |                                                 |   |
           +----->[ delay 1 ]------------------gain 1------->|   |
           |                                                 | + |
           +---------->[delay 2]---------------gain 2------->|   |
           :                                                 |   |
           :                                                 |   |
           +--------------->[ delay n ]--------gain n------->|___|
                                                               | 
                                                               |
                                                               +--gain out---> y
'''


def echo(x, sample_rate, echo_delays, echo_gains, gain_in=1, gain_out=1):
    echo_delays = np.int_(np.asarray(echo_delays) * sample_rate)
    max_delay = np.max(echo_delays)
    delay_line = np.zeros(max_delay)
    delay_pos = 0
    y = np.zeros_like(x)

    for i, sample in enumerate(x):
        y[i] = gain_in * sample  # Initialize with the input sample

        for j, delay in enumerate(echo_delays):
            target = (delay_pos - delay) % len(delay_line)
            y[i] += echo_gains[j] * delay_line[target]

        delay_line[delay_pos] = sample
        delay_pos = (delay_pos + 1) % len(delay_line)

    return y * gain_out


class Echo():
    def __init__(self, sample_rate, echo_delays, echo_gains, gain_in=1, gain_out=1):
        self.echo_delays = np.int_(np.asarray(echo_delays) * sample_rate)
        max_delay = np.max(self.echo_delays)
        self.delay_line = Delay(max_delay)
        self.gain_in = gain_in
        self.gain_out = gain_out
        self.echo_gains = echo_gains

    def process(self, x):
        y = self.gain_in * x
        for i, delay in enumerate(self.echo_delays):
            y += self.echo_gains[i] * self.delay_line.go_back(delay)
        self.delay_line.push(x)
        return self.gain_out * y
