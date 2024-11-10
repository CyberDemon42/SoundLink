import time
from pydub.generators import Sine
import simpleaudio as sa

def bin_to_sound(a):
    b = []
    b.append(8000)
    for i in a:
        if i == "0":
            b.append(4500)
        elif i == "1":
            b.append(7500)
    return b

def sound_speaker(seq_in_sound):
    for frequency in seq_in_sound:
        duration = 200

        sine_wave = Sine(frequency).to_audio_segment(duration=duration)

        play_obj = sa.play_buffer(
            sine_wave.raw_data,
            num_channels=1,
            bytes_per_sample=2,
            sample_rate=sine_wave.frame_rate
        )

        time.sleep(0.08)
