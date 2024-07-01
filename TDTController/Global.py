import tdt
import numpy as np


class TDTGlobal:
    def __init__(self, config=None):
        self.syn = tdt.SynapseAPI()
        # self.audio = self.AuditoryStimulus(config, self.syn)
        self.audio = self.NaturalStimulusSet(self.syn)

    def start_recording(self):
        self.syn.setMode(3)

    def stop_recording(self):
        self.syn.setMode(0)

    class AuditoryStimulus:
        def __init__(self, config, tdt_module):
            self.config = config['auditory_config']

            self.tdt_module = tdt_module
            self.tdt_module.setParameterValue('ToneStim', 'PulseDur', int(self.config['audio_duration_ms']))
            self.tdt_module.setParameterValue('NoiseStim', 'PulseDur', int(self.config['audio_duration_ms']))

            max_freq = 6000
            min_freq = 440

            step = ((max_freq + 1) - min_freq) / 12

            self.levels = np.arange(start=min_freq, stop=max_freq, step=step)

            # levels = np.logspace(-2., 5., num=63)

        def present(self, i):
            if i is not None:
                # draw the stimuli and update the window
                if i < 12:
                    self.tdt_module.setParameterValue('StimSel', 'ChanSel-1', 1)
                    self.tdt_module.setParameterValue('SyncSel', 'ChanSel-1', 1)
                    self.tdt_module.setParameterValue('ToneStim', 'WaveFreq', self.levels[i])
                    self.tdt_module.setParameterValue('ToneStim', 'Strobe', 1)

                else:
                    self.tdt_module.setParameterValue('StimSel', 'ChanSel-1', 2)
                    self.tdt_module.setParameterValue('SyncSel', 'ChanSel-1', 2)
                    self.tdt_module.setParameterValue('NoiseStim', 'Strobe', 1)

    class NaturalStimulusSet:
        def __init__(self, tdt_module):
            self.tdt_module = tdt_module
            duration = 500

            self.tdt_module.setParameterValue('ToneStim', 'PulseDur', int(duration))
            self.tdt_module.setParameterValue('NoiseStim', 'PulseDur', int(duration))

            max_freq = 8000
            min_freq = 400

            step = ((max_freq + 1) - min_freq) / 12

            self.levels = np.arange(start=min_freq, stop=max_freq, step=step)

            # levels = np.logspace(-2., 5., num=63)

        def present_tone(self, i):
            if i < len(self.levels):
                # draw the stimuli and update the window
                self.tdt_module.setParameterValue('StimSelector', 'ChanSel-1', 2)
                self.tdt_module.setParameterValue('SyncSelector', 'ChanSel-1', 2)
                self.tdt_module.setParameterValue('ToneStim', 'WaveFreq', self.levels[i])
                self.tdt_module.setParameterValue('Trigger', 'Button1', 1)
                return f"P-{self.levels[i]}-500"
            else:
                return f"P-{i}-Failed"

        def present_noise(self):
            self.tdt_module.setParameterValue('StimSelector', 'ChanSel-1', 3)
            self.tdt_module.setParameterValue('SyncSelector', 'ChanSel-1', 3)
            self.tdt_module.setParameterValue('Trigger', 'Button1', 1)
            return f"N-500"

        def present_file(self, i):
            self.tdt_module.setParameterValue('StimSelector', 'ChanSel-1', 1)
            self.tdt_module.setParameterValue('SyncSelector', 'ChanSel-1', 1)
            self.tdt_module.setParameterValue('AudioStim', 'ID', i)
            self.tdt_module.setParameterValue('Trigger', 'Button1', 1)
            return f"F-{i}"