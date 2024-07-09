import json
import numpy as np

# Generate amplitudes from -3 to 9 with step 1
# amplitudes = np.arange(10, 81, 10).tolist()

stimuli = [{'id': 1, 'duration_ms': 17000}, {'id': 2, 'duration_ms': 18000}, {'id': 3, 'duration_ms': 50000}] * 5

# Create the JSON structure

data = {
    "duration_ms": 200,
    "inter_stimulus_interval_ms": 800,
    "shuffle": True,
    "stimuli": stimuli
}

# Save to a JSON file
with open("../assets/experiments_jsons/rat_vocalization.json", "w") as f:
    json.dump(data, f, indent=4)
