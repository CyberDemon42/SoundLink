import numpy as np
import pyaudio
from scipy.fftpack import fft

# Parameters
CHUNK = 4096  # Number of samples per frame
FORMAT = pyaudio.paInt32  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 32000  # Sampling rate
LOWER_RANGE = (4000, 5000)  # Lower frequency range to detect
UPPER_RANGE = (7000, 8000)  # Upper frequency range to detect
AMPLITUDE_THRESHOLD = 50  # Threshold for amplitude detection (adjust as needed)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening...")

a=[]

def detect_frequencies(data, rate, chunk, lower_range, upper_range, threshold, a):
    # Convert audio data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Perform FFT
    yf = fft(audio_data)
    xf = np.fft.fftfreq(chunk, 1 / rate)

    # Normalize the magnitude of the FFT
    magnitude = np.abs(yf[:chunk // 2]) / chunk

    detected = False

    # Check the lower frequency range
    lower_index = np.where((xf[:chunk // 2] >= lower_range[0]) & (xf[:chunk // 2] <= lower_range[1]))[0]
    if np.any(magnitude[lower_index] > threshold):
        detected = True
        print(f"Detected frequency in range {lower_range[0]}-{lower_range[1]} Hz")
        a.append(0)

    # Check the upper frequency range
    upper_index = np.where((xf[:chunk // 2] >= upper_range[0]) & (xf[:chunk // 2] <= upper_range[1]))[0]
    if np.any(magnitude[upper_index] > threshold):
        detected = True
        print(f"Detected frequency in range {upper_range[0]}-{upper_range[1]} Hz")
        a.append(1)

    print(a)

    return detected

try:
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)

        # Detect target frequency ranges with high amplitude
        detect_frequencies(data, RATE, CHUNK, LOWER_RANGE, UPPER_RANGE, AMPLITUDE_THRESHOLD, a)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
