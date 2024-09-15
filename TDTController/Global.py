import scipy
import tdt
import numpy as np
from typing import Literal


class TDTGlobal:
    def __init__(self, config=None):
        self.syn = tdt.SynapseAPI()
        self.cache = {}
        self.calibration_map = None
        self.calibrator = Calibrator(type="ES")
        print("Hello from TDTGlobal")
        # self.audio = self.AuditoryStimulus(config, self.syn)
        # self.audio = self.NaturalStimulusSet(self.syn)

    def switch_to_experiment(self, exp_name):
        known_exp = self.syn.getKnownExperiments()
        assert exp_name in known_exp, f"The defined experiment {exp_name} " \
                                      f"is not defined in the synapse. Please choose from {known_exp}"
        self.syn.setCurrentExperiment(exp_name)
        self.cache['AudioStim'] = self.get_stimulation_gizmos('AudioStim')
        self.cache['FileStim'] = self.get_stimulation_gizmos('FileStim')
        self.cache['UserInput'] = self.get_stimulation_gizmos('UserInput')
        self.cache['uStim'] = self.get_stimulation_gizmos('uStim')

    def get_all_active_gizmos(self):
        return self.syn.getGizmoNames()

    def get_stimulation_gizmos(self, gizmo_type: Literal['FileStim', 'AudioStim', 'UserInput', 'uStim']):
        all_gizmos = self.get_all_active_gizmos()
        found = []
        for gizmo in all_gizmos:
            info = self.syn.getGizmoInfo(gizmo)
            if info['type'] == gizmo_type:
                found.append(gizmo)
        return found

    def start_recording(self):
        self.syn.setMode(3)

    def stop_recording(self):
        self.syn.setMode(0)

    def _calibrate_amp(self, freq, amp):
        if self.calibration_map is None:
            return amp - 80

    def _us_calibrate_amp(self, freq, amp):
        if self.calibration_map is None:
            return amp

    def play_audio_stimulation(self, freq=None, duration_ms=None, amplitude=None):
        trigger_gizmo = self.cache["UserInput"][0]
        for gizmo_name in self.cache['AudioStim']:
            if duration_ms is not None:
                self.syn.setParameterValue(gizmo_name, 'PulseDur', duration_ms)
            if freq is not None:
                self.syn.setParameterValue(gizmo_name, 'WaveFreq', freq)
            if amplitude is not None:
                self.syn.setParameterValue(gizmo_name, 'WaveAmp', self._calibrate_amp(freq, amplitude))

        self.syn.setParameterValue(trigger_gizmo, 'Button1', 1)

    def play_file_stimulation(self, file_id=None):
        trigger_gizmo = self.cache["UserInput"][0]
        for gizmo_name in self.cache['FileStim']:
            if file_id is not None:
                self.syn.setParameterValue(gizmo_name, 'ID', file_id)
        self.syn.setParameterValue(trigger_gizmo, 'Button1', 1)

    def play_white_noise_stimulation(self, duration_ms=None, amplitude=None):
        trigger_gizmo = self.cache["UserInput"][0]
        for gizmo_name in self.cache['AudioStim']:
            if duration_ms is not None:
                self.syn.setParameterValue(gizmo_name, 'PulseDur', duration_ms)
            if amplitude is not None:
                self.syn.setParameterValue(gizmo_name, 'WaveAmp', self._calibrate_amp(0, amplitude))
        self.syn.setParameterValue(trigger_gizmo, 'Button1', 1)

    def play_ultrasonic_stimulation(self, freq=None, duration_ms=None, amplitude=None):
        trigger_gizmo = self.cache["UserInput"][0]
        for gizmo_name in self.cache['uStim']:
            if duration_ms is not None:
                self.syn.setParameterValue(gizmo_name, 'WaveDur', duration_ms)
            if freq is not None:
                self.syn.setParameterValue(gizmo_name, 'WaveFreq', freq)
            # TODO: if require this calibration or not (-80 dB)
            if amplitude is not None:
                self.syn.setParameterValue(gizmo_name, 'WaveAmp', self.calibrator.adjust_amplitude(freq, amplitude))

        self.syn.setParameterValue(trigger_gizmo, 'Button1', 1)

    def get_recording_tank(self):
        return self.syn.getCurrentTank()

    def get_sampling_rate(self):
        return self.syn.getSamplingRates()

    # TODO: add functions to set the fixed parameters of the gizmos

    # class AuditoryStimulus:
    #     def __init__(self, config, tdt_module):
    #         self.config = config['auditory_config']
    #
    #         self.tdt_module = tdt_module
    #         self.tdt_module.setParameterValue('LFS', 'PulseDur', int(self.config['audio_duration_ms']))
    #         self.tdt_module.setParameterValue('Noise', 'PulseDur', int(self.config['audio_duration_ms']))
    #
    #         max_freq = 6000
    #         min_freq = 440
    #
    #         step = ((max_freq + 1) - min_freq) / 12
    #
    #         self.levels = np.arange(start=min_freq, stop=max_freq, step=step)
    #
    #         # levels = np.logspace(-2., 5., num=63)
    #
    #     def present(self, i):
    #         if i is not None:
    #             # draw the stimuli and update the window
    #             if i < 12:
    #                 self.tdt_module.setParameterValue('StimSel', 'ChanSel-1', 1)
    #                 self.tdt_module.setParameterValue('SyncSel', 'ChanSel-1', 1)
    #                 self.tdt_module.setParameterValue('ToneStim', 'WaveFreq', self.levels[i])
    #                 self.tdt_module.setParameterValue('ToneStim', 'Strobe', 1)
    #
    #             else:
    #                 self.tdt_module.setParameterValue('StimSel', 'ChanSel-1', 2)
    #                 self.tdt_module.setParameterValue('SyncSel', 'ChanSel-1', 2)
    #                 self.tdt_module.setParameterValue('NoiseStim', 'Strobe', 1)
    #
    # class NaturalStimulusSet:
    #     def __init__(self, tdt_module):
    #         self.tdt_module = tdt_module
    #         duration = 500
    #
    #         self.tdt_module.setParameterValue('LFTone', 'PulseDur', int(duration))
    #         self.tdt_module.setParameterValue('NoiseStim', 'PulseDur', int(duration))
    #
    #         max_freq = 8000
    #         min_freq = 400
    #
    #         step = ((max_freq + 1) - min_freq) / 12
    #
    #         self.levels = np.arange(start=min_freq, stop=max_freq, step=step)
    #
    #         # levels = np.logspace(-2., 5., num=63)
    #
    #     def present_tone(self, i):
    #         if i < len(self.levels):
    #             # draw the stimuli and update the window
    #             # self.tdt_module.setParameterValue('WavSel', 'ChanSel-1', 1)
    #             # self.tdt_module.setParameterValue('SynSel', 'ChanSel-1', 1)
    #             self.tdt_module.setParameterValue('LFTone', 'WaveFreq', self.levels[i])
    #             self.tdt_module.setParameterValue('Trigger', 'Button1', 1)
    #             return f"P-{self.levels[i]}-500"
    #         else:
    #             return f"P-{i}-Failed"
    #
    #     def present_noise(self):
    #         self.tdt_module.setParameterValue('WavSel', 'ChanSel-1', 3)
    #         self.tdt_module.setParameterValue('SynSel', 'ChanSel-1', 3)
    #         self.tdt_module.setParameterValue('SWTrig', 'Button1', 1)
    #         return f"N-500"
    #
    #     def present_file(self, i):
    #         self.tdt_module.setParameterValue('WavSel', 'ChanSel-1', 2)
    #         self.tdt_module.setParameterValue('SynSel', 'ChanSel-1', 2)
    #         self.tdt_module.setParameterValue('NFS', 'ID', i)
    #         self.tdt_module.setParameterValue('SWTrig', 'Button1', 1)
    #         return f"F-{i}"


class Calibrator:
    def __init__(self, type='ES'):
        if type == 'ES':
            calibration_data = np.loadtxt(
                'C:/Users/Lomber/Desktop/Npx-Experiment/Experiments/assets/calibrations/es_lookup_table.txt')
        else:
            calibration_data = np.loadtxt(
                'C:/Users/Lomber/Desktop/Npx-Experiment/Experiments/assets/calibrations/mf_lookup_table.txt')
        self.sr = 200000
        self.frequencies = calibration_data[:, 0]
        self.magnitude_dB = calibration_data[:, 1]

        # Create an interpolation function for the calibration data
        self.interp_func = scipy.interpolate.interp1d(self.frequencies, self.magnitude_dB, kind='linear',
                                                      fill_value="extrapolate")

    def adjust_amplitude(self, frequency, amplitude):
        """
        Adjust the amplitude of a tone based on the calibration data.

        Parameters:
        frequency (float): Frequency of the tone
        amplitude (float): Desired amplitude of the tone

        Returns:
        float: Adjusted amplitude
        """
        if amplitude < 80:
            amplitude = 1 / ((80 - amplitude) / 5)
        else:
            amplitude = 1

        frequency = frequency / (self.sr / 2)  # Normalize the frequency (0 to 0.5 for normalized frequency
        print(amplitude, frequency)

        cal_dB = self.interp_func(frequency)
        adjusted_amp = amplitude * 10 ** (cal_dB / 20)
        return adjusted_amp
