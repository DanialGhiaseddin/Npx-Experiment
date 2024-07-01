from random import shuffle

from TDTController.Global import TDTGlobal
import time
import logging
import time
from datetime import datetime
from tqdm import tqdm


# Set up logging
log_filename = f"stimulus_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

Description = "First Cold Run with Set3"
logging.info(Description)

stim_set = [f"P-{i}" for i in range(12)] * 5 + ["N"] * 10 + [f"F-{i}" for i in range(1, 30)] * 5

# shuffle(stim_set)

# stim_set = stim_set

shuffle(stim_set)

print(stim_set)
print(len(stim_set))

tdt_manager = TDTGlobal()

tdt_manager.start_recording()

time.sleep(10)

for stim in tqdm(stim_set):
    if "P" in stim:
        m = tdt_manager.audio.present_tone(int(stim.split('-')[1]))
        logging.info(f"Stimulus presented - {m}")
        time.sleep(2)
    elif "N" in stim:
        m = tdt_manager.audio.present_noise()
        logging.info(f"Stimulus presented - {m}")
        time.sleep(2)
    elif "F" in stim:
        m = tdt_manager.audio.present_file(int(stim.split('-')[1]))
        logging.info(f"Stimulus presented - {m}")
        time.sleep(6)

tdt_manager.stop_recording()
logging.shutdown()
