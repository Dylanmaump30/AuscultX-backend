import os
import numpy as np
from src.audioprocess import Butterworth as butter
from src.audioprocess import Hilbert as hilbert
from scipy.signal import find_peaks
from scipy.ndimage import uniform_filter1d
from matplotlib import pyplot as plt
from scipy.io import wavfile 
import math

CUT_FREQ = [250, 2250] 
def normalize_audio(amp):
    if amp.dtype == np.int16:
        return amp.astype(np.float32) / 32768
    elif amp.dtype == np.int32:
        return amp.astype(np.float32) / 2147483648
    elif amp.dtype == np.uint8:
        return (amp.astype(np.float32) - 128) / 128
    return amp.astype(np.float32)

def clip_signal(signal):
    mean = np.mean(signal)
    std = np.std(signal)
    return np.clip(signal, mean - 3 * std, mean + 3 * std)

def estimate_peaks(signal, fs):
    duration = len(signal) / fs
    est_inhales = duration / 1.0
    min_distance = int(fs * (duration / est_inhales) * 0.5)
    threshold = np.percentile(signal, 35)
    prominence = np.percentile(signal, 25) * 0.9
    peaks, properties = find_peaks(
        signal, height=threshold, distance=min_distance, prominence=prominence, 
    )
    rpm = math.ceil(((len(peaks) / 2) / duration) * 60)

    return peaks, threshold, len(peaks), rpm, duration

def process_audio(audio_path):
    if not os.path.exists(audio_path):
        print(f"Error: Audio file '{audio_path}' not found.")
        return None

    fs, amp = wavfile.read(audio_path)
    amp = normalize_audio(amp)

    original_signal = clip_signal(amp.copy())
    filtered_signal = clip_signal(butter.filter_audio(amp=amp, fs=fs, cut_freq=CUT_FREQ, ftype='band'))
    envelope_signal = hilbert.envelope(filtered_signal, fs=fs)
    final_signal = butter.filter_audio(amp=envelope_signal, fs=fs, cut_freq=CUT_FREQ[0], ftype='low')
    final_signal = uniform_filter1d(final_signal, size=int(fs * 0.15) )
    time = np.linspace(0, len(final_signal) / fs, num=len(final_signal))
    peaks, threshold, n_peaks, rpm, duration = estimate_peaks(final_signal, fs)
    
    return {
        "audio_name": os.path.basename(audio_path),
        "frame_rate": fs,
        "time": time.tolist(),
        "original_signal": original_signal.tolist(),  
        "filtered_signal": filtered_signal.tolist(),  
        "envelope_signal": envelope_signal.tolist(),  
        "final_signal": final_signal.tolist(),        
        "n_peaks": n_peaks, 
        "rpm": rpm
    }  