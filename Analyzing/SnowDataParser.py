import pickle
from os import path

import tdt

from Analyzing.signal.processing import relative_crop
from GraphicalInterface.utils.log import parse_log_file
import pandas as pd
from tqdm import tqdm

recording_directory = ('/home/danial/Documents/Projects/McGill/Npx-Experiment/Analyzing/data/tdt '
                       'tanks/Subject1-231219-160734')

tdt_data = tdt.read_block(recording_directory)

esc50_dir = '/home/danial/Documents/Projects/McGill/Npx-Experiment/Stimulus Preprocessing/ESC-50-master/audio_test/'

esc50_df = pd.read_csv(
    '/home/danial/Documents/Projects/McGill/Npx-Experiment/Stimulus Preprocessing/ESC-50-master/meta/esc50.csv')

log_file = (
    '/home/danial/Documents/Projects/McGill/Npx-Experiment/Analyzing/data/tdt tanks/Subject1-231219-160734/stimulus_log_20231219_160734.log')

_, stim_orders = parse_log_file(log_file)

onsets = tdt_data['epocs'].Tr1_.onset
offsets = tdt_data['epocs'].Tr1_.offset

with (open(path.join(recording_directory, 'TDT_Presentation.csv')) as f):
    played_stimuli = f.readlines()[0].split(',')
played_stimuli = [stimulus.split('||')[0] for stimulus in played_stimuli]
index_to_name_map = {}
name_to_index_map = {}
for i, stimulus in enumerate(played_stimuli):
    index_to_name_map[i + 1] = stimulus
    name_to_index_map[stimulus] = i + 1

result_dict = {}

for i, stimulus in tqdm(enumerate(stim_orders)):
    if 'F-' in stimulus:
        key = index_to_name_map[int(stimulus.split('-')[1])]
    else:
        key = stimulus
    if key not in result_dict:
        result_dict[key] = []

    signal_names_list = ['RSTM', 'RSYN', 'LFPR', 'NEUR']

    trial = {}

    for signal_name in signal_names_list:
        data = tdt_data['streams'][signal_name]['data']
        sample_rate = float(tdt_data['streams'][signal_name]['fs'])

        exp_duration = tdt_data['info']['duration']
        exp_duration = float(f"{exp_duration.seconds}.{exp_duration.microseconds}")

        start_index = (onsets[i] - 0.5) / exp_duration
        end_index = (onsets[i] + 5.5) / exp_duration

        f_signal = relative_crop(data, start_index, end_index)

        trial[signal_name] = {'data': f_signal, 'sample_rate': sample_rate}

    result_dict[key].append(trial)

with open('session3.pkl', 'wb') as handle:
    pickle.dump(result_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Saved!")

# stim_file = played_stimuli[self.disp_stim_index]
#
# self.audio_file_name.set(stim_file)
#
# self.audio_file_path = path.join(self.audio_set_directory, stim_file)
#
# self.audio_file_category.set(
#     self.esc50_df.loc[self.esc50_df['filename'] == stim_file, 'category'].values[0])
#
# selected_trials = self.find_trials(stim_file)
#
# self.selected_onsets = self.onsets[selected_trials]
# self.selected_offsets = self.offsets[selected_trials]
# self.plot()
