from datetime import timedelta

import numpy as np
import pandas as pd


# DISCLAIMER: This function is copied from https://github.com/nwhitehead/swmixer/blob/master/swmixer.py,
#             which was released under LGPL.
def resample_by_interpolation(signal, input_fs, output_fs):
    scale = output_fs / input_fs
    # calculate new length of sample
    n = round(len(signal) * scale)

    # use linear interpolation
    # endpoint keyword means than linspace doesn't go all the way to 1.0
    # If it did, there are some off-by-one errors
    # e.g. scale=2.0, [1,2,3] should go to [1,1.5,2,2.5,3,3]
    # but with endpoint=True, we get [1,1.4,1.8,2.2,2.6,3]
    # Both are OK, but since resampling will often involve
    # exact ratios (i.e. for 44100 to 22050 or vice versa)
    # using endpoint=False gets less noise in the resampled sound
    resampled_signal = np.interp(
        np.linspace(0.0, 1.0, n, endpoint=False),  # where to interpret
        np.linspace(0.0, 1.0, len(signal), endpoint=False),  # known positions
        signal,  # known data points
    )
    return resampled_signal


def normalization(signal):
    signal = (signal - np.min(signal))
    signal = (signal / np.max(signal))
    return signal


def relative_crop(signal, start_point, end_point):
    start_index = start_point * signal.shape[-1]
    end_index = end_point * signal.shape[-1]

    if len(signal.shape) == 1:
        filtered_signal = signal[int(start_index):int(end_index)]
    else:
        filtered_signal = signal[:, int(start_index):int(end_index)]
    return filtered_signal


def digitize(signal, threshold=None):
    if threshold is None:
        threshold = np.mean(signal)
    signal[signal <= threshold] = 0
    signal[signal > threshold] = 1
    return signal


def remove_noise_pulses(subject_signal, duration):
    filtered_signal = subject_signal.copy()
    diff = np.diff(subject_signal)
    edge_indices = np.where(diff != 0)[0]
    times = pd.timedelta_range(start='0:0:0.000', end=duration, periods=subject_signal.shape[0])
    edges = times._data[edge_indices]
    pulses = edges[1:] - edges[0:-1]
    eps = timedelta(hours=0, minutes=0, seconds=0.050,
                    microseconds=0)
    for i, pulse_time in enumerate(pulses):
        if pulse_time < eps:
            filtered_signal[edge_indices[i]:edge_indices[i + 1] + 1] = filtered_signal[edge_indices[i]]

    return filtered_signal


def rectify_noise_pulses(subject_signal, duration):
    filtered_signal = subject_signal.copy()
    diff = np.diff(subject_signal)
    edge_indices = np.where(diff != 0)[0]
    times = pd.timedelta_range(start='0:0:0.000', end=duration, periods=subject_signal.shape[0])
    edges = times._data[edge_indices]
    pulses = edges[1:] - edges[0:-1]
    eps = timedelta(hours=0, minutes=0, seconds=0.050,
                    microseconds=0)
    for i, pulse_time in enumerate(pulses):
        if pulse_time < eps:
            filtered_signal[edge_indices[i]:edge_indices[i + 1] + 1] = 1

    return filtered_signal


def find_rising_edges(subject_signal, duration):
    diff = np.diff(subject_signal)
    rising_indices = np.where(diff > 0)[0]
    times = pd.timedelta_range(start='0:0:0.000', end=duration, periods=subject_signal.shape[0])
    raising_edges = times._data[rising_indices]
    return raising_edges, rising_indices


def find_pulse_length(subject_signal, duration):
    diff = np.diff(subject_signal)
    edge_indices = np.where(diff != 0)[0]
    times = pd.timedelta_range(start='0:0:0.000', end=duration, periods=subject_signal.shape[0])
    edges = times._data[edge_indices]
    pulses = edges[1:] - edges[0:-1]
    return pulses, edge_indices
