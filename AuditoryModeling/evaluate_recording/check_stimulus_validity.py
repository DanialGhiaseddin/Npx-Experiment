import pickle

from matplotlib.figure import Figure
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

from signal_processing import resample_by_interpolation

with open('/home/danial/Documents/Projects/Personal/AuditoryModeling/data/recording_data/session1.pkl', 'rb') as handle:
    recording = pickle.load(handle)

stimulus_number = 9

stimulus = sorted(list(recording.keys()))[stimulus_number]

audio_file = '/home/danial/Documents/Projects/Personal/AuditoryModeling/data/esc_50/audio/' + stimulus

print(stimulus)

fig = plt.figure(figsize=(5, 4))

# fig, ax = plt.subplots()

plot_channels = len(recording[stimulus]) * 2 + 1

# read audio samples
sr, audio = read(audio_file)

audio = resample_by_interpolation(audio, sr, recording[stimulus][0]['RSTM']['sample_rate'])

plot = fig.add_subplot(plot_channels, 1, 1)
plot.plot(audio)

for plot_index, trial in enumerate(recording[stimulus]):
    f_signal = trial['RSYN']['data']
    sample_rate = trial['RSYN']['sample_rate']
    print(sample_rate)
    plot = fig.add_subplot(plot_channels, 1, (plot_index + 1) * 2)
    plot.plot(f_signal)

    f_signal = trial['RSTM']['data']
    sample_rate = trial['RSTM']['sample_rate']
    print(sample_rate)
    plot = fig.add_subplot(plot_channels, 1, (plot_index + 1) * 2 + 1)
    plot.plot(f_signal)

# label the axes
# set the title
# display the plot
fig.show()
