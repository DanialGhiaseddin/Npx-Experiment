import random

from SpikeGLX.controller import SpikeGLXHandler
from TDTController.Global import TDTGlobal
import logging
import time
from datetime import datetime
from Logger import Logger
import json
from utils import get_function_name


class SessionHandler:
    def __init__(self, master, sender="Test", penetration_location="Unknown"):
        self.master = master
        self.tdt = master.tdt
        self.penetration_location = penetration_location
        self.logger = Logger(f"session_logs//{datetime.now().strftime('%Y%m%d_%H%M%S')}_{sender}.log")

        self.incremental = False
        self.sender = sender

        self.global_info = {
            'test_with_pure_tones': {
                'number_of_sub_sessions': 1,
                'tdt_experiment': ['LFTone'],
                'functions': [self.pure_tone_stimulation],
                'json_files': ['test_with_pure_tones.json']
            },
            'test_with_white_noises': {
                'number_of_sub_sessions': 1,
                'tdt_experiment': ['WhiteNoise'],
                'functions': [self.noise_stimulation],
                'json_files': ['test_with_white_noises.json']
            },
            'test_with_natural_stimuli': {
                'number_of_sub_sessions': 1,
                'tdt_experiment': ['FileStimShort'],
                'functions': [self.file_stimulation],
                'json_files': ['test_with_natural_stimuli.json']
            },

            'test_with_ultrasonic_tones': {
                'number_of_sub_sessions': 1,
                'tdt_experiment': ['HFTone'],
                'functions': [self.ultrasonic_stimulation],
                'json_files': ['test_with_ultrasonic_tones.json']
            },

            'lf_tuning_curve': {
                'number_of_sub_sessions': 3,
                'tdt_experiment': ['LFTone', 'LFTone', 'LFTone'],
                'functions': [self.pure_tone_stimulation, self.pure_tone_stimulation, self.pure_tone_stimulation],
                'json_files': ['lf_tuning_curve.json', 'lf_tuning_curve.json', 'lf_tuning_curve.json']
            },
            'hf_tuning_curve': {
                'number_of_sub_sessions': 3,
                'tdt_experiment': ['HFTone', 'HFTone', 'HFTone'],
                'functions': [self.ultrasonic_stimulation, self.ultrasonic_stimulation, self.ultrasonic_stimulation],
                'json_files': ['hf_tuning_curve.json', 'hf_tuning_curve.json', 'hf_tuning_curve.json']
            }
        }

        # if "natural_stimuli_ext" in sender:
        #     self.incremental = True
        #     self.session_number = int(sender.split("_")[-1])
        #     self.global_info[sender] = {
        #         'number_of_sub_sessions': 2,
        #         'tdt_experiment': [f'FSetE{2 * self.session_number}', f'FSetE{2 * self.session_number + 1}'],
        #         'functions': [self.file_stimulation, self.file_stimulation],
        #         'json_files': ['natural_stimuli.json', 'natural_stimuli.json']
        #     }
        if "natural_stimuli_" in sender:
            self.incremental = True
            self.session_number = int(sender.split("_")[-1])
            self.global_info[sender] = {
                'number_of_sub_sessions': 1,
                'tdt_experiment': [f'FileSet{self.session_number}'],
                'functions': [self.file_stimulation],
                'json_files': ['natural_stimuli.json']
            }
        elif "ultrasonic_vocalization" in sender:
            self.incremental = True
            self.session_number = int(sender.split("_")[-1])
            if self.session_number == 0:
                self.global_info[sender] = {
                    'number_of_sub_sessions': 1,
                    'tdt_experiment': [f'USFileSetMouse'],
                    'functions': [self.file_stimulation],
                    'json_files': ['mouse_vocalization.json']
                }
            else:
                self.global_info[sender] = {
                    'number_of_sub_sessions': 1,
                    'tdt_experiment': [f'USFileSetRat'],
                    'functions': [self.rat_vocalization_stimulation],
                    'json_files': ['rat_vocalization.json']
                }
        elif "av_stimuli_random" in sender:
            self.incremental = True
            self.session_number = int(sender.split("_")[-1])
            self.global_info[sender] = {
                'number_of_sub_sessions': 1,
                'tdt_experiment': [f'XB_Exp2'],
                'functions': [self.av_stimulation],
                'json_files': [f'av_stimulation_random_{self.session_number}.json']
            }

        elif "av_stimuli" in sender:
            self.incremental = True
            self.session_number = int(sender.split("_")[-1])
            self.global_info[sender] = {
                'number_of_sub_sessions': 1,
                'tdt_experiment': [f'XB_Exp1'],
                'functions': [self.av_stimulation],
                'json_files': ['av_stimulation.json']
            }

        self.info = self.global_info[sender]
        self.run_simulus_presentation = None

        self.spike_glx = SpikeGLXHandler(logger=self.logger)
        self.spike_glx.connect()

        self.write_log(f"Electrode location: {self.penetration_location}")

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

            self.run_simulus_presentation = self.info['functions'][sub_session]

            json_file = self.info['json_files'][sub_session]

            self.write_log(f"TDT experiment switched to {self.info['tdt_experiment'][sub_session]}")
            self.write_log(self.tdt.get_sampling_rate())
            self.write_log(f"Data will be saved to {self.tdt.get_recording_tank()}")

            if enable_neuropixel_recording and not break_run:
                self.spike_glx.start_recording()
                #set_neuropixel_recording(True)  # TODO: Communicate better with Neuropixel
                self.write_log("Starting neuropixel system...")
                time.sleep(2)

            self.write_log("Starting TDT recording...")
            self.tdt.start_recording()
            time.sleep(10)

            # Stimulus Presentation
            self.write_log("Starting Stimulus Presentation")
            try:
                self.run_simulus_presentation(sub_session_num=sub_session, json_file=json_file)
            except StopIteration as e:
                self.write_log(e, log_type='error')
                break_run = True

            self.write_log("Stopping TDT recording...")
            self.tdt.stop_recording()
            if enable_neuropixel_recording:
                self.spike_glx.stop_recording()
                # set_neuropixel_recording(False)  # TODO: Communicate better with Neuropixel
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
            if self.incremental:
                self.master.increment_session_number('_'.join(self.sender.split("_")[:-1]))
        else:
            self.write_log(f"Session terminated with emergency break or other exceptions.")
        # TODO: if necessary, apply autoincrement
        self.logger.close()

    # def lf_tuning_curve(self, sub_session_num):
    #     func_name = get_function_name()
    #
    #     with open(f"assets/experiments_jsons/{func_name}.json", "r") as f:
    #         data = json.load(f)
    #
    #     self._pure_tone_stimulation(sub_session_num, data)
    #
    # def test_with_pure_tones(self, sub_session_num):
    #     func_name = get_function_name()
    #

    #     self._pure_tone_stimulation(sub_session_num, data)

    def pure_tone_stimulation(self, sub_session_num, json_file):
        # Load the JSON file

        with open(f"assets/experiments_jsons/{json_file}", "r") as f:
            data = json.load(f)

        progress_factor = 100 // self.info['number_of_sub_sessions']

        # Extract the list of stimuli
        delay_s = (data.get("inter_stimulus_interval_ms", 800) + data.get("duration_ms", 200)) / 1000
        duration_ms = data.get("duration_ms", 200)
        stimuli = data.get("stimuli", [])
        if data.get("shuffle", True):
            random.shuffle(stimuli)
        for i, stimulus in enumerate(stimuli):
            if self.master.emergency_break:
                raise StopIteration("Emergency break requested.")
            self.tdt.play_audio_stimulation(freq=stimulus['freq'], amplitude=(stimulus['amp']), duration_ms=duration_ms)
            self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}")
            time.sleep(delay_s)
            self.master.update_progress(
                percent=((progress_factor * sub_session_num) + int((i + 1) / len(stimuli) * progress_factor)))

    def noise_stimulation(self, sub_session_num, json_file):
        # Load the JSON file

        with open(f"assets/experiments_jsons/{json_file}", "r") as f:
            data = json.load(f)

        progress_factor = 100 // self.info['number_of_sub_sessions']

        # Extract the list of stimuli
        delay_s = (data.get("inter_stimulus_interval_ms", 800) + data.get("duration_ms", 200)) / 1000
        duration_ms = data.get("duration_ms", 200)
        stimuli = data.get("stimuli", [])
        if data.get("shuffle", True):
            random.shuffle(stimuli)
        for i, stimulus in enumerate(stimuli):
            if self.master.emergency_break:
                raise StopIteration("Emergency break requested.")
            self.tdt.play_white_noise_stimulation(amplitude=(stimulus['amp']), duration_ms=duration_ms)
            self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}")
            time.sleep(delay_s)
            self.master.update_progress(
                percent=((progress_factor * sub_session_num) + int((i + 1) / len(stimuli) * progress_factor)))

    def file_stimulation(self, sub_session_num, json_file):
        with open(f"assets/experiments_jsons/{json_file}", "r") as f:
            data = json.load(f)

        progress_factor = 100 // self.info['number_of_sub_sessions']

        # Extract the list of stimuli
        delay_s = (data.get("inter_stimulus_interval_ms", 800) + data.get("duration_ms", 200)) / 1000
        duration_ms = data.get("duration_ms", 200)
        stimuli = data.get("stimuli", [])
        if data.get("shuffle", True):
            random.shuffle(stimuli)
        for i, stimulus in enumerate(stimuli):
            if self.master.emergency_break:
                raise StopIteration("Emergency break requested.")
            self.tdt.play_file_stimulation(file_id=(stimulus['id']))
            self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}")
            time.sleep(delay_s)
            self.master.update_progress(
                percent=((progress_factor * sub_session_num) + int((i + 1) / len(stimuli) * progress_factor)))

    def ultrasonic_stimulation(self, sub_session_num, json_file):
        # Load the JSON file

        with open(f"assets/experiments_jsons/{json_file}", "r") as f:
            data = json.load(f)

        progress_factor = 100 // self.info['number_of_sub_sessions']

        # Extract the list of stimuli
        delay_s = (data.get("inter_stimulus_interval_ms", 800) + data.get("duration_ms", 200)) / 1000
        duration_ms = data.get("duration_ms", 200)
        stimuli = data.get("stimuli", [])
        if data.get("shuffle", True):
            random.shuffle(stimuli)
        for i, stimulus in enumerate(stimuli):
            if self.master.emergency_break:
                raise StopIteration("Emergency break requested.")
            self.tdt.play_ultrasonic_stimulation(freq=stimulus['freq'], amplitude=(stimulus['amp']),
                                                 duration_ms=duration_ms)
            self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}")
            time.sleep(delay_s)
            self.master.update_progress(
                percent=((progress_factor * sub_session_num) + int((i + 1) / len(stimuli) * progress_factor)))

    def rat_vocalization_stimulation(self, sub_session_num, json_file):

        with open(f"assets/experiments_jsons/{json_file}", "r") as f:
            data = json.load(f)

        progress_factor = 100 // self.info['number_of_sub_sessions']

        # Extract the list of stimuli
        isi_s = (data.get("inter_stimulus_interval_ms", 800)) / 1000
        # duration_ms = data.get("duration_ms", 200)
        stimuli = data.get("stimuli", [])
        if data.get("shuffle", True):
            random.shuffle(stimuli)
        for i, stimulus in enumerate(stimuli):
            if self.master.emergency_break:
                raise StopIteration("Emergency break requested.")
            self.tdt.play_file_stimulation(file_id=(stimulus['id']))
            self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}")
            time.sleep(isi_s + (stimulus['duration_ms'] / 1000))
            self.master.update_progress(
                percent=((progress_factor * sub_session_num) + int((i + 1) / len(stimuli) * progress_factor)))

    def av_stimulation(self, sub_session_num, json_file):
        with open(f"assets/experiments_jsons/{json_file}", "r") as f:
            data = json.load(f)

        progress_factor = 100 // self.info['number_of_sub_sessions']

        # Extract the list of stimuli
        stimuli = data.get("stimuli", [])
        for i, stimulus in enumerate(stimuli):
            if self.master.emergency_break:
                raise StopIteration("Emergency break requested.")
            self.tdt.play_file_stimulation(file_id=(stimulus['id']))
            self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}")
            delay = stimulus['delay_s']
            while delay > 0:
                self.write_log(f"Playing: {i + 1}/{len(stimuli)}: {stimulus}, Remaining: {delay} seconds.")
                time.sleep(1)
                if self.master.emergency_break:
                    raise StopIteration("Emergency break requested.")
                delay -= 1
            self.master.update_progress(
                percent=((progress_factor * sub_session_num) + int((i + 1) / len(stimuli) * progress_factor)))
