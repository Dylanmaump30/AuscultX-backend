from scipy.signal import butter,filtfilt

CUT_FREQ = 2250.0


def filter_audio(amp, fs, cut_freq=CUT_FREQ, ftype='low'):
  
    b, a = butter(6, cut_freq, fs=fs, btype=ftype)

    return filtfilt(b, a, amp)