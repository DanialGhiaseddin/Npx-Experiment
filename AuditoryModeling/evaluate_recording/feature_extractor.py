import math
import pickle

from .common_processing import crop_trials, find_pulse_length, find_envelope, split_signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.spatial import distance as dis
import numpy as np

from gamma import remove_gamma_band
from signal_processing import resample_by_interpolation, relative_crop, normalization_symmetric
from tqdm import tqdm


def extract_features(recording, window_size=0.300, session=1):
    final_dict = {}

    for stimulus_number in tqdm(range(0, len(recording.keys()))):

        stimulus = sorted(list(recording.keys()))[stimulus_number]
        # print(stimulus)

        if '.wav' in stimulus:
            audio_file = '/home/danial/Documents/Projects/Personal/AuditoryModeling/data/esc_50/audio/' + stimulus
            audio_sr, audio = read(audio_file)
            expected_length = 4.516
        else:
            expected_length = 0.516

        # Initial Cropping

        '''
        Steps to be done for feature extraction
        1. Align_signal: Split the signal into windows (500) ms data -> 15 Tokens (No overlap) -> just enough to align
            * We have stimulus wavfile with new sampling rate
        2. Based on the stimulus -> Find The mask for each token
        3. For each trial:
            1. If trial is not complete -> Discard
            2. Apply the pre-processing if required
                1. Time Delay
                2. Gamma Band
            3. Segment the signal into windows
            4. take time average
        4. Average Across Trials
        dictionary: {features: [] , mask: [], trials: #, windows_size: #, class:<>, played_time }
        '''
        # 1. Align_signals and find completed trials
        trial_mask = []
        tdt_dac_sr = None
        for trial_idx, trial in enumerate(recording[stimulus]):
            cropped = crop_trials(trial, length=expected_length + 0.1)
            recording[stimulus][trial_idx] = cropped

            sync_pulse = cropped['RSYN']['data']
            sync_sr = cropped['RSYN']['sample_rate']
            p_edge, n_edge = find_pulse_length(sync_pulse)
            pulse_length = n_edge / sync_sr - p_edge / sync_sr
            if math.fabs(pulse_length - expected_length) < 0.002:
                trial_mask.append(True)
                if tdt_dac_sr is None:
                    tdt_dac_sr = 5 / (n_edge / sync_sr - p_edge / sync_sr) * 44100
            else:
                trial_mask.append(False)

        # print("TDT DAC SR: ", tdt_dac_sr)
        # 2. Find the mask for each token
        ref_trial_cand = [i for i, x in enumerate(trial_mask) if x]
        if len(ref_trial_cand) > 0:
            ref_trial = ref_trial_cand[0]  # First Completed Trial
        else:
            print(stimulus, "No Completed")
            continue
        stim_signal = recording[stimulus][ref_trial]['RSTM']['data']
        stim_signal = normalization_symmetric(stim_signal)
        stimulus_envelope = find_envelope(stim_signal)
        stimulus_sr = recording[stimulus][ref_trial]['RSTM']['sample_rate']
        segmented_envelope = split_signal(stimulus_envelope, sr=stimulus_sr, window=window_size)
        segment_mask = []
        # plt.plot(stimulus_envelope)
        # plt.show()
        for segment in segmented_envelope:
            # plt.plot(segment)
            # plt.show()
            # print(np.max(segment), np.mean(segment))
            if np.mean(segment) > 0.05:
                segment_mask.append(True)
            else:
                segment_mask.append(False)

        # print(segment_mask)

        lfp_avg_features = []
        # 3. For each trial:
        for trial_idx, trial in enumerate(recording[stimulus]):
            # 1. If trial is not complete -> Discard

            if trial_mask[trial_idx]:
                lpf_signal = recording[stimulus][trial_idx]['LFPR']['data']
                lpf_sr = recording[stimulus][trial_idx]['LFPR']['sample_rate']

                # 2. Apply the pre-processing if required
                #     1. Time Delay
                #     2. Gamma Band
                # lpf_signal = remove_gamma_band(lpf_signal, sampling_freq=lpf_sr)
                # 3. Segment the signal into windows
                segmented_lpf = split_signal(lpf_signal, sr=lpf_sr, window=window_size)

                # 4. take time average
                lfp_single_trial_features = []
                for segment in segmented_lpf:
                    lfp_feature = np.mean(segment, axis=1)
                    lfp_feature = np.expand_dims(lfp_feature, axis=0)
                    lfp_single_trial_features.append(lfp_feature)
                lfp_single_trial_features = np.concatenate(lfp_single_trial_features, axis=0)
                lfp_single_trial_features = np.expand_dims(lfp_single_trial_features, axis=0)
                lfp_avg_features.append(lfp_single_trial_features)
            else:  # Discard the trial
                pass
        lfp_avg_features = np.concatenate(lfp_avg_features, axis=0)
        # 4. Average Across Trials
        result = {'features': lfp_avg_features, 'mask': segment_mask, 'good_trials': lfp_avg_features.shape[0],
                  'windows_size': window_size, 'category': 'Cat', 'tdt_dac_sr': tdt_dac_sr}

        if ".wav" not in stimulus:
            stimulus += f"-{str(session)}"
        final_dict[stimulus] = result

    return final_dict


if __name__ == '__main__':
    window_ms = 0.300
    session = 3
    with open(f'/home/danial/Documents/Projects/Personal/AuditoryModeling/data/recording_data/session{session}.pkl',
              'rb') as handle:
        recording_dict = pickle.load(handle)

    features = extract_features(recording_dict, window_size=window_ms)

    with open(f'../data/features/session{session}_features.pkl', 'wb') as handle:
        pickle.dump(features, handle, protocol=pickle.HIGHEST_PROTOCOL)
