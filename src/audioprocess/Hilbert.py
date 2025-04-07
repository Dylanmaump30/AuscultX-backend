import numpy as np
from scipy.signal import hilbert


def envelope(signal, fs=44100):
    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)
    amp_min, amp_max = np.min(amplitude_envelope), np.max(amplitude_envelope)
    amp_norm = (amplitude_envelope - amp_min) / (amp_max - amp_min)


    return amp_norm
