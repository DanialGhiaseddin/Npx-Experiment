import pickle

from matplotlib.figure import Figure
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

from gamma import remove_gamma_band
from signal_processing import resample_by_interpolation

with open('/home/danial/Documents/Projects/Personal/AuditoryModeling/data/recording_data/session2.pkl', 'rb') as handle:
    recording = pickle.load(handle)

print(sorted(list(recording.keys())))

for i, stim in enumerate(sorted(list(recording.keys()))):
    print(i, stim)

stimulus_number = 56
trial_number = 4
start_channel = 0

stimulus = sorted(list(recording.keys()))[stimulus_number]

print(stimulus)

fig = plt.figure(figsize=(5, 4))

plot_channels = 10

# audio = resample_by_interpolation(audio, sr, recording[stimulus][0]['RSTM']['sample_rate'])

target_sr = recording[stimulus][trial_number]['LFPR']['sample_rate']

f_signal = recording[stimulus][trial_number]['RSYN']['data']
sample_rate = recording[stimulus][trial_number]['RSYN']['sample_rate']
f_signal = resample_by_interpolation(f_signal, sample_rate, target_sr)
plot = fig.add_subplot(plot_channels, 1, 1)
plot.plot(f_signal)

f_signal = recording[stimulus][trial_number]['RSTM']['data']
sample_rate = recording[stimulus][trial_number]['RSTM']['sample_rate']
f_signal = resample_by_interpolation(f_signal, sample_rate, target_sr)
plot = fig.add_subplot(plot_channels, 1, 2)
plot.plot(f_signal)

for c in range(8):
    f_signal = recording[stimulus][trial_number]['LFPR']['data'][start_channel + c]
    # f_signal = remove_gamma_band(f_signal, sampling_freq=target_sr)
    gamma_removed = remove_gamma_band(f_signal, sampling_freq=target_sr)
    plot = fig.add_subplot(plot_channels, 1, c + 3)
    plot.plot(gamma_removed)
    # plot.plot(f_signal)

# label the axes
# set the title
# display the plot
fig.show()
