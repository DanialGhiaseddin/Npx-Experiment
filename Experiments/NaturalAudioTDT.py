from SpikeGLX.controller import set_neuropixel_recording
from TDTController.Global import TDTGlobal
import logging
import time
from datetime import datetime


def play_lf_tone(tk_component, enable_recording):
    tk_component.toggle_ui_state('disabled')

    experiment = 'LFTone'
    print(experiment)
    tdt_manager = TDTGlobal(config=None)

    result = tdt_manager.syn.setCurrentExperiment(experiment)

    assert result == 1

    if enable_recording:
        set_neuropixel_recording(True)
        tk_component.write_log(f"Setting Up the neuropixel")
        time.sleep(2)

    tk_component.write_log(f"Starting TDT System")

    time.sleep(10)

    # Set up logging
    log_filename = f"experiment_logs//stimulus_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    description = f"Stimulus Set: {experiment}"
    logging.info(description)

    # stim_set = [f"P-{i}" for i in range(12)] * 5 + ["N"] * 10 +

    stim_set = [f"P-{i}" for i in range(12)]

    # shuffle(stim_set)

    # stim_set = stim_set

    # shuffle(stim_set)

    print(stim_set)
    print(len(stim_set))

    tdt_manager.start_recording()

    tk_component.write_log("Starting TDT System...")
    time.sleep(10)
    tk_component.write_log("Starting Stimulus Presentation...")
    for i, stim in enumerate(stim_set):
        if "P" in stim:
            m = tdt_manager.audio.present_tone(int(stim.split('-')[1]))
            logging.info(f"Stimulus presented - {m}")
            time.sleep(0.5)
        elif "N" in stim:
            m = tdt_manager.audio.present_noise()
            logging.info(f"Stimulus presented - {m}")
            time.sleep(2)
        elif "F" in stim:
            m = tdt_manager.audio.present_file(int(stim.split('-')[1]))
            logging.info(f"Stimulus presented - {m}")
            time.sleep(6)
        tk_component.update_progress(percent=int((i + 1) / len(stim_set) * 100))
        tk_component.write_log(f"Stimulus presented - {m}")
    tk_component.write_log("Stimulus Presentation Done...")
    time.sleep(10)
    tdt_manager.stop_recording()
    tk_component.write_log("TDT Recording Stopped Successfully...")

    if enable_recording:
        set_neuropixel_recording(False)
        tk_component.write_log(f"Stopping the neuropixel")
        time.sleep(2)

    logging.shutdown()
    tk_component.toggle_ui_state('normal')


def play_natural_stimulus_set(session_number, ses_id, tk_component, enable_recording=True):
    tk_component.toggle_ui_state('disabled')

    experiment = f'StimSet{session_number.get()}'
    print(experiment)
    tdt_manager = TDTGlobal(config=None)

    result = tdt_manager.syn.setCurrentExperiment(experiment)

    assert result == 1

    if enable_recording:
        set_neuropixel_recording(True)
        tk_component.write_log(f"Setting Up the neuropixel")
        time.sleep(2)

    time.sleep(5)

    # Set up logging
    log_filename = f"experiment_logs//stimulus_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    description = f"Stimulus Set: {experiment}"
    logging.info(description)

    # stim_set = [f"P-{i}" for i in range(12)] * 5 + ["N"] * 10 +

    stim_set = [f"F-{i}" for i in range(1, 30)] * 5

    # shuffle(stim_set)

    # stim_set = stim_set

    # shuffle(stim_set)

    print(stim_set)
    print(len(stim_set))

    tdt_manager.start_recording()

    tk_component.write_log("Starting TDT System...")
    time.sleep(10)
    tk_component.write_log("Starting Stimulus Presentation...")
    for i, stim in enumerate(stim_set):
        if "P" in stim:
            m = tdt_manager.audio.present_tone(int(stim.split('-')[1]))
            logging.info(f"Stimulus presented - {m}")
            time.sleep(1)
        elif "N" in stim:
            m = tdt_manager.audio.present_noise()
            logging.info(f"Stimulus presented - {m}")
            time.sleep(2)
        elif "F" in stim:
            m = tdt_manager.audio.present_file(int(stim.split('-')[1]))
            logging.info(f"Stimulus presented - {m}")
            time.sleep(6)
        tk_component.update_progress(percent=int((i + 1) / len(stim_set) * 100))
        tk_component.write_log(f"Stimulus presented - {m}")
    tk_component.write_log("Stimulus Presentation Done...")
    time.sleep(10)
    tdt_manager.stop_recording()
    tk_component.write_log("TDT Recording Stopped Successfully...")

    if enable_recording:
        set_neuropixel_recording(False)
        tk_component.write_log(f"Stopping the neuropixel")
        time.sleep(2)

    logging.shutdown()
    tk_component.toggle_ui_state('normal')
    tk_component.increment_session_number(ses_id)
    # tk_component.session_number_variables[simulus_set].set(tk_component.session_number_variables[simulus_set].get() + 1)
    # session_number.set(session_number.get() + 1)
