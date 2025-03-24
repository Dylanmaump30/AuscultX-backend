from pydub import AudioSegment as am
import os

def convert_to_mono(audio, freq=44100, dst_folder='src/files/audios/'):

    sound = am.from_file(audio, format='wav')
    sound = sound.set_frame_rate(freq).set_channels(1)        
    new_audio = f'{dst_folder}audio_mono.wav'
    sound.export(new_audio, format='wav')
    return new_audio, sound.frame_rate

