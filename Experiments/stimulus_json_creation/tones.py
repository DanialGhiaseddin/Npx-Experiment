import json
import numpy as np

# Starting frequency and number of octaves
start_freq = 1000
num_octaves = 5
fundamentals = [8400, 11200, 15840]

frequencies = []
# Generate logarithmic frequencies
for f in fundamentals:
    frequencies += [f]
    for i in range(num_octaves):
        frequencies.append(frequencies[-1] * 2)

n_frequencies = []
for f in frequencies:
    if f <= 100000:
        n_frequencies.append(f)

frequencies = n_frequencies

frequencies = sorted(frequencies)

# Generate amplitudes from -3 to 9 with step 1
# amplitudes = np.arange(10, 81, 10).tolist()

amplitudes = [10, 20, 30, 40, 50, 60, 70, 80]

# Create the JSON structure
stimuli = [{"freq": round(freq, 2), "amp": round(amp, 2)} for freq in frequencies for amp in amplitudes]

data = {
    "duration_ms": 200,
    "inter_stimulus_interval_ms": 800,
    "shuffle": False,
    "stimuli": stimuli
}

# Save to a JSON file
with open("../assets/experiments_jsons/hf_tuning_curve.json", "w") as f:
    json.dump(data, f, indent=4)
