from Analyzing.signal.processing import relative_crop, resample_by_interpolation, find_pulse_length
from log_file_parser import extract_info_from_log
import tdt
import os
import matplotlib.pyplot as plt
import numpy as np


def calculate_pulse_lengths(signal):
    signal = np.array(signal)
    # Compute the derivative of the signal
    derivative = np.diff(signal)

    # Find indices of rising and falling edges
    rising_edges = np.where(derivative == 1)[0]
    falling_edges = np.where(derivative == -1)[0]

    # Ensure the rising and falling edges are paired correctly
    if falling_edges[0] < rising_edges[0]:
        falling_edges = falling_edges[1:]
    if len(rising_edges) > len(falling_edges):
        rising_edges = rising_edges[:len(falling_edges)]

    # Calculate pulse lengths
    pulse_lengths = falling_edges - rising_edges

    return pulse_lengths


# Example usage
log_file_path = 'C:/Users/Lomber/Desktop/Npx-Experiment/Experiments/session_logs/20240708_052335_natural_stimuli_15.log'
extracted_sections = extract_info_from_log(log_file_path)

for index, section in enumerate(extracted_sections):

    print(f"Final path for section {index + 1}: {section['tdt_path']}")

    tdt_data = tdt.read_block(section['tdt_path'])

    onsets = tdt_data['epocs'].Tr1_.onset
    offsets = tdt_data['epocs'].Tr1_.offset

    signal_names_list = tdt_data['streams'].keys()

    trial = {}

    stim_orders = section['ids']

    result_dict = {}

    print(calculate_pulse_lengths(tdt_data['streams']['Wav2']['data']))
    print(len(calculate_pulse_lengths(tdt_data['streams']['Wav2']['data'])))

    for i, stimulus in enumerate(stim_orders):

        for signal_name in signal_names_list:
            data = tdt_data['streams'][signal_name]['data']
            sample_rate = float(tdt_data['streams'][signal_name]['fs'])

            exp_duration = tdt_data['info']['duration']
            exp_duration = float(f"{exp_duration.seconds}.{exp_duration.microseconds}")

            start_index = (onsets[i] - 0.5) / exp_duration
            end_index = (onsets[i] + 5.5) / exp_duration

            f_signal = relative_crop(data, start_index, end_index)
            plt.plot(f_signal)
            plt.show()
            # f_signal = resample_by_interpolation(f_signal, sample_rate, 1000)
            trial[signal_name] = {'data': f_signal, 'sample_rate': sample_rate}

        result_dict[stimulus] = trial
