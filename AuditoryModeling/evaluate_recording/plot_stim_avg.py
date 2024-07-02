import pickle

from matplotlib.figure import Figure
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np

from evaluate_recording.common_processing import crop_trials
from gamma import remove_gamma_band, notch_filter
from signal_processing import resample_by_interpolation


def get_trial_avg(stimulus_name, signal_name, resample_rate=None):
    avg_signal = None
    for trial_idx, trial in enumerate(recording[stimulus_name]):
        signal = trial[signal_name]['data']
        initial_sr = trial[signal_name]['sample_rate']
        if len(signal.shape) == 1:
            if resample_rate is not None:
                signal = resample_by_interpolation(signal, initial_sr, resample_rate)
            if avg_signal is None:
                avg_signal = np.zeros((len(recording[stimulus_name]), signal.shape[-1] + 10))
            avg_signal[trial_idx] = np.pad(signal, (0, avg_signal.shape[-1] - signal.shape[-1]), 'constant')
        else:
            for c in range(signal.shape[0]):
                if resample_rate is not None:
                    signal_c = resample_by_interpolation(signal[c], initial_sr, resample_rate)
                    signal_c = remove_gamma_band(signal_c, sampling_freq=resample_rate)
                else:
                    signal_c = signal[c]
                if avg_signal is None:
                    avg_signal = np.zeros((len(recording[stimulus_name]), signal.shape[0], signal.shape[-1] + 10))
                avg_signal[trial_idx, c] = np.pad(signal_c, (0, avg_signal.shape[-1] - signal.shape[-1]), 'constant')
    avg_signal = np.mean(avg_signal, axis=0)
    return avg_signal


with open('/home/danial/Documents/Projects/Personal/AuditoryModeling/data/recording_data/session2.pkl', 'rb') as handle:
    recording = pickle.load(handle)

print(sorted(list(recording.keys())))

stimulus_number = 56
start_channel = 10

stimulus = sorted(list(recording.keys()))[stimulus_number]

if '.wav' in stimulus:
    length = 5
else:
    length = 0.5

for trial_idx, trial in enumerate(recording[stimulus]):
    cropped = crop_trials(trial, length=length)
    recording[stimulus][trial_idx] = cropped

print(stimulus)

fig = plt.figure(figsize=(5, 4))

plot_channels = 10

# audio = resample_by_interpolation(audio, sr, recording[stimulus][0]['RSTM']['sample_rate'])

target_sr = recording[stimulus][0]['LFPR']['sample_rate']

f_signal = get_trial_avg(stimulus, 'RSYN', target_sr)
plot = fig.add_subplot(plot_channels, 1, 1)
plot.plot(f_signal)

f_signal = get_trial_avg(stimulus, 'RSTM', target_sr)
plot = fig.add_subplot(plot_channels, 1, 2)
plot.plot(f_signal)

f_signal = get_trial_avg(stimulus, 'LFPR', target_sr)
for c in range(8):
    plot = fig.add_subplot(plot_channels, 1, c + 3)
    # gamma_removed = notch_filter(f_signal[start_channel + c], f0=100, fs=target_sr)
    gamma_removed = f_signal[start_channel + c]
    # gamma_removed = remove_gamma_band(f_signal[start_channel + c], sampling_freq=target_sr)
    plot.plot(gamma_removed)


# label the axes
# set the title
# display the plot
fig.show()
