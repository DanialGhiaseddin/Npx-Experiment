import json
import numpy as np

# Starting frequency and number of octaves
start_freq = 1000
num_octaves = 5
fundamentals = [1050, 1400, 1980]

frequencies = []
# Generate logarithmic frequencies
for f in fundamentals:
    frequencies += [f]
    for i in range(num_octaves):
        frequencies.append(frequencies[-1] * 2)

n_frequencies = []
for f in frequencies:
    if f <= 48000:
        n_frequencies.append(f)

frequencies = n_frequencies


frequencies = sorted(frequencies)

# Generate amplitudes from -3 to 9 with step 1
amplitudes = np.arange(10, 81, 10).tolist()

# Create the JSON structure
stimuli = [{"freq": round(freq, 2), "amp": round(amp, 2)} for freq in frequencies for amp in amplitudes]

data = {
    "duration_ms": 200,
    "stimuli": stimuli
}

# Save to a JSON file
with open("frequencies_log_scale.json", "w") as f:
    json.dump(data, f, indent=4)
