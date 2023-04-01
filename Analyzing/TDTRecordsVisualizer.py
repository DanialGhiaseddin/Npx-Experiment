from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
import tdt
from termcolor import colored

from Analyzing.signal.processing import resample_by_interpolation, relative_crop, normalization, remove_noise_pulses, find_rising_edges


times = pd.timedelta_range(start='0:0:0.440', end='0:0:40.000', periods=2000)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print(
        colored("-----------------------TDT Data Reader---------------------------------------------------", "yellow"))
    data = tdt.read_block('E:/Npx-Experiment/Analyzing/data/tdt tanks/Subject1-230331-144025')
    print(
        colored("-----------------------Data Recording Analyzer-------------------------------------------", "yellow"))
    print('Start Date:', data['info']['start_date'])
    print('Stop Date:', data['info']['stop_date'])
    print('Duration:', data['info']['duration'])
    exp_duration = data['info']['duration']
    print(
        colored("-----------------------------------------------------------------------------------------", "yellow"))

    continue_flag = False

    raw_data = []
    sample_rates = []

    while not continue_flag:

        print(colored("Please select signal(s) from the list. Please split names with comma:", "blue"))
        print(data['streams'].keys())
        try:
            command = input(colored('>>', 'green'))
            command = command.replace('"', '')
            command = command.replace("'", '')

            signal_names_list = "".join(command.split()).split(',')

            for signal_name in signal_names_list:
                raw_data.append(data['streams'][signal_name]['data'])
                sample_rates.append(float(data['streams'][signal_name]['fs']))

            # print(raw_data)
            print(sample_rates)
            continue_flag = True
        except (TypeError, ValueError, AttributeError) as err:
            print(colored(err, 'red'))
            continue_flag = False

    print(
        colored("-----------------------------------------------------------------------------------------", "yellow"))

    continue_flag = False
    start_idx = 0
    end_idx = 1
    while not continue_flag:
        try:
            print(colored("Please enter the start time, '%H:%M:%S.%f'", "blue"))
            start_time = input(colored('>>', 'green'))
            start_time = datetime.strptime(start_time, '%H:%M:%S.%f').time()
            start_time = timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second,
                                   microseconds=start_time.microsecond)

            assert start_time < exp_duration, "Invalid start time"
            start_idx = start_time / exp_duration

            print(colored("Please enter the end time, '%H:%M:%S.%f'", "blue"))
            end_time = input(colored('>>', 'green'))
            end_time = datetime.strptime(end_time, '%H:%M:%S.%f').time()
            end_time = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second,
                                 microseconds=end_time.microsecond)

            assert end_time <= exp_duration, "Invalid end time"
            assert start_time < end_time, "Start time should be less than end time"

            end_idx = end_time / exp_duration

            print(
                colored("-----------------------------------------------------------------------------------------",
                        "yellow"))

            continue_flag = True

        except (Exception, AssertionError) as ex:
            print(colored(ex, 'red'))
            continue_flag = False

    fig, axs = plt.subplots(len(raw_data))

    for i, raw_data_sig in enumerate(raw_data):
        f_signal = relative_crop(raw_data_sig, start_idx, end_idx)
        f_signal = normalization(f_signal)
        f_signal = resample_by_interpolation(f_signal, sample_rates[i], 8000)

        times = pd.timedelta_range(start=start_time, end=end_time, periods=f_signal.shape[0])

        axs[i].plot(times._data, f_signal)
    plt.show()
