#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn
import random


TTL_ZERO_LIMIT = .8
TTL_ONE_LIMIT = 2.
TTL_VCC = 5.


class Signal(object):

    def __init__(self, signal, time):
        self.signal = signal
        self.time = time
        self.nvals = len(self.signal)
        self.resolution = self.time[1] - self.time[0]


def analog_to_digital(signal):
    def ttl_to_digital(val):
        if val <= TTL_ZERO_LIMIT:
            return 0
        elif val >= TTL_ONE_LIMIT:
            return 1
        else:
            return random.randint(0, 1)

    return list(map(ttl_to_digital, signal))


def generate_bouncy_signal(pre_sec=.05, delay_sec=.002, post_sec=.05,
                           time_step_sec=.001, settled_noise=.2):
    duration = pre_sec + delay_sec + post_sec
    time = np.linspace(0.0, duration, int(duration / time_step_sec + 1))

    # Create pre bouncing signal
    analog_signal = [(randn() * settled_noise)
                     for _ in range(int(pre_sec / time_step_sec))]
    # Create bouncing noise
    analog_signal.extend([(TTL_VCC / 2 + randn() * 1.2)
                         for _ in range(int(delay_sec / time_step_sec))])
    # Create post bouncing signal
    analog_signal.extend([(TTL_VCC + randn() * settled_noise)
                         for _ in range(int(post_sec / time_step_sec) + 1)])

    digital_signal = analog_to_digital(analog_signal)
    return Signal(analog_signal, time), Signal(digital_signal, time)


class Debouncer(object):

    def __init__(self, check_sec=0.005, press_sec=0.01, release_sec=0.1):
        self.check_sec = check_sec
        self.press_sec = press_sec
        self.release_sec = release_sec

        self.debounced_key_press = False
        self.count = int(self.release_sec / self.check_sec)

    def debounce(self, raw_state):
        key_changed = False
        key_pressed = self.debounced_key_press
        raw_state = bool(raw_state)
        if raw_state == self.debounced_key_press:
            if self.debounced_key_press:
                self.count = int(self.release_sec / self.check_sec)
            else:
                self.count = int(self.press_sec / self.check_sec)
        else:
            self.count -= 1
            if self.count == 0:
                self.debounced_key_press = raw_state
                key_changed = True
                key_pressed = self.debounced_key_press
                if self.debounced_key_press:
                    self.count = int(self.release_sec / self.check_sec)
                else:
                    self.count = int(self.press_sec / self.check_sec)

        return key_changed, key_pressed


def plot_switch_waveforms(analog, digital, debounced):
    ax1 = plt.subplot(311)
    ax1.set_yticks([0., TTL_ZERO_LIMIT, TTL_ONE_LIMIT, TTL_VCC])
    plt.plot(analog.time, analog.signal, label='analog', lw=1)
    plt.grid(True)
    plt.ylabel('TTL voltage (V)')

    ax2 = plt.subplot(312)
    ax2.set_yticks([0, 1])
    plt.plot(digital.time, digital.signal, label='digital', lw=1)
    plt.grid(True)
    plt.ylabel('Logic value')

    ax3 = plt.subplot(313)
    ax3.set_yticks([0, 1])
    plt.plot(debounced.time, debounced.signal, label='digital', lw=1)
    plt.grid(True)
    plt.ylabel('Logic value')

    plt.xlabel('time (s)')

    plt.show()


if __name__ == "__main__":

    # Instatiate the Debouncer
    db = Debouncer(check_sec=0.005, press_sec=0.015, release_sec=0.1)

    # Generate the bouncy button press signal
    analog, digital = generate_bouncy_signal(delay_sec=0.02)

    # Calculate sampling points on the bouncy signal
    duration = (digital.nvals - 1) * digital.resolution
    sample_points = int(np.round(duration / db.check_sec) + 1)

    new_points = np.linspace(0., duration, sample_points)
    new_points = [int(np.round((digital.nvals-1) * (i / new_points[-1]), 0))
                  for i in new_points]

    # Debounce the signal
    dbs = []
    for i in new_points:
        key_changed, key_pressed = db.debounce(digital.signal[i])
        dbs.append(key_pressed)

    debounced = Signal(dbs, [i / 1000. for i in new_points])

    # Plot the signals
    plot_switch_waveforms(analog, digital, debounced)
