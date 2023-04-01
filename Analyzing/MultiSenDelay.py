import matplotlib.pyplot as plt
import pandas as pd
import tdt
from termcolor import colored

from Analyzing.signal.processing import normalization, remove_noise_pulses, find_rising_edges, digitize, \
    rectify_noise_pulses

times = pd.timedelta_range(start='0:0:0.440', end='0:0:40.000', periods=2000)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = tdt.read_block('E:/Npx-Experiment/Analyzing/data/tdt tanks/Subject1-230331-144507')
    print(
        colored("-----------------------Data Recording Analyzer-------------------------------------------", "yellow"))
    print('Start Date:', data['info']['start_date'])
    print('Stop Date:', data['info']['stop_date'])
    print('Duration:', data['info']['duration'])
    exp_duration = data['info']['duration']
    print(
        colored("-----------------------------------------------------------------------------------------", "yellow"))
    print(data['streams'].keys())

    audio = data['streams']['Sync']['data']
    video = data['streams']['Diod']['data']

    audio = normalization(audio)
    audio = digitize(audio)
    audio = rectify_noise_pulses(audio, exp_duration)

    audio_rising_edge = find_rising_edges(audio, duration=exp_duration)

    video = normalization(video)
    video = digitize(video)
    video = remove_noise_pulses(video, exp_duration)

    video_rising_edge = find_rising_edges(video, duration=exp_duration)
    # plt.plot(audio[0000:200000])
    # plt.plot(audio2[0000:200000])
    plt.plot(audio[0000:2000000])
    plt.plot(video[0000:2000000] / 2)
    plt.show()
    print(len(audio_rising_edge[0]))
    print(len(video_rising_edge[0]))
