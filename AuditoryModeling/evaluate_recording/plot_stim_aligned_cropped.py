import math
import pickle

from common_processing import crop_trials, find_pulse_length, find_envelope
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.spatial import distance as dis

from gamma import remove_gamma_band
from signal_processing import resample_by_interpolation, relative_crop, normalization_symmetric

stimulus_number = 20
start_channel = 0

with open('/home/danial/Documents/Projects/Personal/AuditoryModeling/data/recording_data/session3.pkl', 'rb') as handle:
    recording = pickle.load(handle)

print(sorted(list(recording.keys())))

for i, stim in enumerate(sorted(list(recording.keys()))):
    print(i, stim)

stimulus = sorted(list(recording.keys()))[stimulus_number]

print(stimulus)

audio_file = '/home/danial/Documents/Projects/Personal/AuditoryModeling/data/esc_50/audio/' + stimulus

sr, audio = read(audio_file)

if '.wav' in stimulus:
    length = 5
else:
    length = 0.5

for trial_idx, trial in enumerate(recording[stimulus]):
    cropped = crop_trials(trial, length=length)
    recording[stimulus][trial_idx] = cropped

for trial_idx in range(5):
    sync_pulse = recording[stimulus][trial_idx]['RSYN']['data']
    sync_sr = recording[stimulus][trial_idx]['RSYN']['sample_rate']
    p_edge, n_edge = find_pulse_length(sync_pulse)
    print(n_edge/sync_sr - p_edge/sync_sr)
    print(5 / (n_edge/sync_sr - p_edge/sync_sr) * 44100)

# sr_ranges = [(i * 10) + 48000 for i in range(0, 201)]
# audio = resample_by_interpolation(audio, 49100, recording[stimulus][0]['RSTM']['sample_rate'])
# distances = []
# min_dist = 100000
# best_sr = 0
# for sr in sr_ranges:
#     played_stimuli = recording[stimulus][0]['RSTM']['data']
#     played_stimuli = find_envelope(played_stimuli)
#     audio_temp = resample_by_interpolation(audio, sr, recording[stimulus][0]['RSTM']['sample_rate'])
#     audio_temp = find_envelope(audio_temp)
#     played_stimuli = played_stimuli[:len(audio_temp)]
#     distance = dis.correlation(played_stimuli, audio_temp)
#     # distance = math.sqrt(sum((played_stimuli - audio_temp) ** 2) / len(played_stimuli))
#     if distance < min_dist:
#         min_dist = distance
#         best_sr = sr
#     distances.append(distance)
#
# print(min_dist, best_sr)
#
# plt.plot(sr_ranges, distances)
# plt.show()


audio = resample_by_interpolation(audio, 48825, recording[stimulus][0]['RSTM']['sample_rate'])

fig = plt.figure(figsize=(5, 4))

plot_channels = 5

# ref_signal = recording[stimulus][0]['RSYN']['data']
# align_point = find_rising_edge(ref_signal)[0]
# crop_point = align_point + 1000


for trial_idx in range(5):
    trial = crop_trials(recording[stimulus][trial_idx], length=5.0)

    f_signal = trial['RSYN']['data']

    played_stimuli = trial['RSTM']['data']

    played_stimuli = normalization_symmetric(played_stimuli)

    audio = normalization_symmetric(audio)

    plot = fig.add_subplot(plot_channels, 1, 1 + trial_idx)
    plot.plot(f_signal)
    plot.plot(played_stimuli)
    # plot.plot(audio - played_stimuli[:len(audio)], color='red')
    plot.plot(audio, color='black')
# label the axes
# set the title
# display the plot
fig.show()
