import json
import numpy as np

# Starting frequency and number of octaves

ids = [i+1 for i in range(36)] * 5

# Create the JSON structure
stimuli = [{"id": id_num} for id_num in ids]

data = {
    "duration_ms": 200,
    "inter_stimulus_interval_ms": 300,
    "shuffle": True,
    "stimuli": stimuli
}

# Save to a JSON file
with open("../assets/experiments_jsons/mouse_vocalization.json", "w") as f:
    json.dump(data, f, indent=4)
