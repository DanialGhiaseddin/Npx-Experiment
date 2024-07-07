from SpikeGLX.controller import set_neuropixel_recording
from TDTController.Global import TDTGlobal
import logging
import time
from datetime import datetime
from Logger import Logger
import json


class SessionHandler:
    def __init__(self, master, name="Test"):
        self.master = master
        self.tdt = master.tdt
        self.logger = Logger(f"session_logs//{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.log")

        self.info = {
            'name': name,
            'number_of_sub_sessions': 3,
            'tdt_experiment': ['LFTone', 'LFTone', 'LFTone'],  # TODO: To be determined
            'shuffle_stimuli': True,
        }
        self.run_simulus_presentation = self.lf_tuning_curve

    def write_log(self, message, log_type='info'):

        if log_type == 'info':
            self.logger.info(message)
        else:
            self.logger.error(message)

        self.master.write_log(message)

    def run_session(self, enable_neuropixel_recording=True):
        self.write_log("Session run requested...")
        self.master.update_progress(percent=0)
        self.master.toggle_ui_state('disabled')
        self.master.restart_emergency_break()
        break_run = False
        for sub_session in range(self.info['number_of_sub_sessions']):
            self.write_log(f"Step {sub_session + 1}/{self.info['number_of_sub_sessions']} is starting.")

            self.tdt.switch_to_experiment(self.info['tdt_experiment'][sub_session])

            self.write_log(f"TDT experiment switched to {self.info['tdt_experiment'][sub_session]}")

            if enable_neuropixel_recording and not break_run:
                set_neuropixel_recording(True)  # TODO: Communicate better with Neuropixel
                self.write_log("Starting neuropixel system...")
                time.sleep(2)

            self.write_log("Starting TDT recording...")
            self.tdt.start_recording()
            time.sleep(10)

            # Stimulus Presentation
            self.write_log("Starting Stimulus Presentation")
            try:
                self.run_simulus_presentation(sub_session_num=sub_session)
            except StopIteration as e:
                self.write_log(e, log_type='error')
                break_run = True

            self.write_log("Stopping TDT recording...")
            self.tdt.stop_recording()
            if enable_neuropixel_recording:
                set_neuropixel_recording(False)  # TODO: Communicate better with Neuropixel
                self.write_log("Stopping neuropixel system...")
                time.sleep(1.5)
            time.sleep(2)
            if break_run:
                break
            self.write_log(f"Step {sub_session + 1}/{self.info['number_of_sub_sessions']} is done.")
            # TODO: ADD more details from TDT System

        self.master.toggle_ui_state('normal')
        self.master.update_progress(percent=0)
        if not break_run:
            self.write_log(f"Session completed successfully.")
        else:
            self.write_log(f"Session terminated with emergency break or other exceptions.")
        # TODO: if necessary, apply autoincrement
        self.logger.close()

    def lf_tuning_curve(self, sub_session_num):

        # Load the JSON file

        progress_factor = 100 // self.info['number_of_sub_sessions']

        with open("stimulus_json_creation//lf_tuning_curve.json", "r") as f:
            data = json.load(f)

        # Extract the list of stimuli
        stimuli = data.get("stimuli", [])
        for i, stimulus in enumerate(stimuli):
            if self.master.emergency_break:
                raise StopIteration("Emergency break requested.")
            self.tdt.play_audio_stimulation(freq=stimulus['freq'], amplitude=(stimulus['amp']), duration_ms=200)
            self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}")
            time.sleep(0.8)
            self.master.update_progress(
                percent=((progress_factor * sub_session_num) + int((i + 1) / len(stimuli) * progress_factor)))
