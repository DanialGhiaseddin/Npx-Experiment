import numpy as np

from signal_processing import relative_crop, normalization, normalization_symmetric

import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert


def find_rising_edge(subject_signal):
    diff = np.diff(subject_signal)
    rising_indices = np.where(diff > 0)[0]
    return rising_indices


def find_pulse_length(subject_signal):
    diff = np.diff(subject_signal)
    edge_indices = np.where(diff != 0)[0]
    pos_edge_index = edge_indices[0]
    neg_edge_index = edge_indices[1]
    return pos_edge_index, neg_edge_index


def crop_trials(trial, length=5):
    sync = trial['RSYN']['data']
    sr = trial['RSYN']['sample_rate']
    rising_edge = find_rising_edge(sync)[0]
    crop_point = rising_edge + length * sr
    for key in trial.keys():
        trial[key]['data'] = relative_crop(trial[key]['data'], rising_edge / sync.shape[-1],
                                           crop_point / sync.shape[-1])
    return trial


def split_signal(signal, sr, window=5):
    result = []
    if len(signal.shape) == 1:
        signal = np.expand_dims(signal, axis=0)
    for i in range(0, signal.shape[-1], round(window * sr)):
        result.append(np.squeeze(signal[:, i:i + round(window * sr)]))
    return result[:len(result) - 1]


def find_envelope(y):
    # Calculate onset envelope
    y = normalization_symmetric(y)

    analytic_signal = hilbert(y)

    amplitude_envelope = np.abs(analytic_signal)

    return amplitude_envelope

# Print detected onset times
# print("Detected onset times (in seconds):", onset_times)
