import os
import numpy as np
from src.audioprocess import Butterworth as butter
from src.audioprocess import Hilbert as hilbert
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
from scipy.io import wavfile 

CUT_FREQ = [250, 2250] 

def process_audio(audio_path):
    if not os.path.exists(audio_path):
        print(f"Error: Audio file '{audio_path}' not found.")
        return None


    fs, amp = wavfile.read(audio_path)  
  
    
    original_signal = amp.copy()

    filtered_signal = butter.filter_audio(amp=amp, fs=fs, cut_freq=CUT_FREQ, ftype='band')

    envelope_signal = hilbert.envelope(filtered_signal,fs=fs)

    final_signal = butter.filter_audio(amp=envelope_signal, fs=fs, cut_freq=CUT_FREQ[0], ftype='low')

    time = np.linspace(0, len(final_signal) / fs, num=len(final_signal))  

    adaptive_threshold = np.percentile(final_signal, 90)  
    min_peak_distance = fs * 2  

    peaks, _ = find_peaks(final_signal, height=adaptive_threshold, distance=min_peak_distance)  
    n_peaks = len(peaks)
    duracion_seg = time[-1] - time[0]
    rpm = (n_peaks / duracion_seg) * 60
  
    """plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(time, original_signal, color='#148db6', label="Señal Original")
    plt.title("Señal Original")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")

    plt.subplot(3, 1, 2)
    plt.plot(time, filtered_signal, color='#148db6', label="Señal Filtrada")
    plt.title("Señal Filtrada")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")

    plt.subplot(3, 1, 3)
    plt.plot(time, final_signal, color='#148db6', label="Señal Envolvente")
    plt.scatter(time[peaks], final_signal[peaks], color='black', marker='o', label="Picos detectados")
    plt.title("Señal Envolvente con Picos Detectados")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.legend()

    plt.tight_layout()
    plt.show() 
    """
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
