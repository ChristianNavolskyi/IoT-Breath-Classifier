import os
import time

import numpy

from receiver import Receiver


def sin(frequency, sin_amplitude, x):
    return sin_amplitude * numpy.sin(x * 2 * numpy.pi / frequency) + sin_amplitude


def update():
    counter = 0

    while True:
        print(counter)
        x = counter * 1 / scan_frequency
        receiver.get_sample(value=sin(breath_frequency, amplitude, x))
        time.sleep(1 / scan_frequency)
        counter += 1


breath_frequency = float(os.getenv("breath_freq", 12 / 60))
scan_frequency = int(os.getenv("scan_freq", 500))
amplitude = float(os.getenv("amplitude", 5.0))

receiver = Receiver()
receiver.simulate_sample()
receiver.mainloop()
