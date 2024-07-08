import json
import numpy as np

# Starting frequency and number of octaves

amplitudes = [60, 65, 70, 75] * 20

# Create the JSON structure
stimuli = [{"amp": round(amp, 2)} for amp in amplitudes]

data = {
    "duration_ms": 500,
    "inter_stimulus_interval_ms": 1000,
    "shuffle": True,
    "stimuli": stimuli
}

# Save to a JSON file
with open("../assets/experiments_jsons/test_with_white_noises.json", "w") as f:
    json.dump(data, f, indent=4)
