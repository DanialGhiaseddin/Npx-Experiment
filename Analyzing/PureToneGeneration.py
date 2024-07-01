import numpy as np
import wave
import math

def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone

def save_wave_file(filename, samples, sample_rate=44100):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())

# Frequencies and notes
tones = [
    (400, "G4"),
    (1200, "E5"),
    (2000, "G#5/Ab5"),
    (2800, "D#6/Eb6"),
    (3600, "A6"),
    (4400, "F#7/Gb7"),
    (5200, "C8"),
    (6000, "D#8/Eb8")
]

sample_rate = 44100  # standard sample rate
duration = 1.0  # duration of each tone in seconds

# Generate tones and save to individual files
for frequency, note in tones:
    tone_samples = generate_tone(frequency, duration, sample_rate)
    filename = f"{note.replace('/', '_')}_{frequency}Hz.wav"
    save_wave_file(filename, np.array(tone_samples), sample_rate)
    print(f"Saved {filename}")
