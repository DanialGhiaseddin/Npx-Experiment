import json
import numpy as np

# Generate amplitudes from -3 to 9 with step 1
# amplitudes = np.arange(10, 81, 10).tolist()

stimuli = [{'id': i+6, 'delay_s': 185} for i in range(5)]

# Create the JSON structure

data = {
    "shuffle": False,
    "stimuli": stimuli
}

# Save to a JSON file
with open("../assets/experiments_jsons/ab_stimulation_random_1.json", "w") as f:
    json.dump(data, f, indent=4)
