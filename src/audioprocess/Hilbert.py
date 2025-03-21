import numpy as np
from scipy.signal import hilbert


def envelope(signal, fs=16000):
    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)
    amp_min, amp_max = np.min(amplitude_envelope), np.max(amplitude_envelope)
    amp_norm = (amplitude_envelope - amp_min) / (amp_max - amp_min)

    inst_phase = np.unwrap(np.angle(analytic_signal))
    inst_freq = np.diff(inst_phase) / (2 * np.pi) * fs

    return amp_norm
