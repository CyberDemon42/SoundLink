import numpy as np
import pyaudio
import matplotlib.pyplot as plt

# Parameters
CHUNK = 2048  # Number of samples per frame
FORMAT = pyaudio.paInt32  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 96000  # Sampling rate

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

# Plotting parameters
plt.ion()  # Interactive mode on
fig, (ax1, ax2) = plt.subplots(2, 1)

# Frequency axis
xf = np.linspace(0, RATE // 2, CHUNK // 2)

# Main loop
try:
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Compute the FFT
        yf = np.fft.fft(audio_data)
        yf = np.abs(yf[0:CHUNK // 2]) / CHUNK

        # Clear previous plots
        ax1.cla()
        ax2.cla()

        # Plot time domain
        ax1.plot(audio_data)
        ax1.set_title("Time Domain")
        ax1.set_xlabel("Samples")
        ax1.set_ylabel("Amplitude")

        # Plot frequency domain
        ax2.plot(xf, yf)
        ax2.set_title("Frequency Domain")
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("Amplitude")

        # Update plots
        plt.pause(0.01)

except KeyboardInterrupt:
    print("Stopped Recording")

finally:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.ioff()
    plt.show()