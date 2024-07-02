import os

from pydub import AudioSegment
from pydub.silence import split_on_silence
import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt


def remove_silence(input_file, output_file, silence_threshold=-40):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Convert AudioSegment to NumPy array
    audio_array = np.array(audio.get_array_of_samples())

    # Split the audio on silence
    segments = split_on_silence(audio, silence_thresh=silence_threshold)

    # Concatenate non-silent segments
    output = AudioSegment.silent()
    for segment in segments:
        output += segment

    # Export the result to a new file
    output.export(output_file, format="wav")


def plot_spectrogram(audio_file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file_path)

    # Calculate the spectrogram
    d = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)

    # Plot the spectrogram
    plt.figure(figsize=(12, 8))
    librosa.display.specshow(d, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of {}'.format(audio_file_path))
    plt.show()


def split_audio_by_onsets(input_file, output_folder):
    # Load the audio file
    y, sr = librosa.load(input_file)

    # Calculate onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Find onset events
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)

    # Plot the onset detection results (optional)
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr, alpha=0.5, color='blue')
    plt.vlines(librosa.frames_to_time(onsets), -1, 1, color='r', alpha=0.9, linestyle='--', label='Onsets')
    plt.title('Waveform with Onset Detection')
    plt.show()

    # Split the audio based on onsets
    for i, onset in enumerate(onsets):
        start_time = librosa.frames_to_time(onset)
        end_time = librosa.frames_to_time(onsets[i + 1]) if i + 1 < len(onsets) else librosa.get_duration(y=y, sr=sr)
        segment = y[librosa.time_to_samples(start_time):librosa.time_to_samples(end_time)]
        output_file = f"{output_folder}/segment_{i + 1}.wav"
        # librosa.output.write_wav(output_file, segment, sr)


# Example usage
# input_file = "path/to/your/input/audio.wav"
# output_folder = "path/to/your/output"
# split_audio_by_onsets(input_file, output_folder)


def adaptive_remove_silence(input_file, output_file, silence_percentage=5):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Calculate the average amplitude
    average_amplitude = audio.rms

    # Set the silence threshold as a percentage of the average amplitude
    silence_threshold = average_amplitude * (silence_percentage / 100)

    # Split the audio on silence
    segments = split_on_silence(audio, silence_thresh=silence_threshold)

    # Concatenate non-silent segments
    output = AudioSegment.silent()
    for segment in segments:
        output += segment

    # Export the result to a new file
    output.export(output_file, format="wav")


def generate_binary_signal(input_file, threshold=0.5):
    # Load the audio file
    y, sr = librosa.load(input_file)

    # Calculate onset strength
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Normalize onset strength to be in the range [0, 1]
    onset_env_normalized = (onset_env - onset_env.min()) / (onset_env.max() - onset_env.min())

    # Create a binary signal based on the threshold
    binary_signal = (onset_env_normalized > threshold).astype(np.int_)

    return binary_signal


def plot_binary_signal(binary_signal, sr):
    # Plot the binary signal
    time = np.arange(0, len(binary_signal)) / sr
    plt.figure(figsize=(12, 4))
    plt.plot(time, binary_signal, label='Binary Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Binary Signal')
    plt.title('Binary Signal indicating Stimuli Presence')
    plt.legend()
    plt.show()


# Example usage
if __name__ == "__main__":
    df = pd.read_csv("./ESC-50-master/meta/esc50.csv")
    df = df[df["fold"] == 5]  # 5th fold for testing
    df = df[df["category"] != "brushing_teeth"]
    df = df.reset_index()
    filenames_to_keep = df['filename'].tolist()
    for filename in os.listdir('./ESC-50-master/audio_test'):
        file_path = os.path.join('./ESC-50-master/audio_test', filename)
        if filename not in filenames_to_keep:
            os.remove(file_path)

    # print(df.head())
    # for index, row in df.iterrows():
    #     input_f = "./ESC-50-master/audio/" + row["filename"]
    #     output_f = "./ESC-50-master/audio_without_silence/" + row["filename"]
    #     split_audio_by_onsets(input_f, './ESC-50-master/audio_without_silence/')
    #     plot_spectrogram(input_f)
    #     binary_signal = generate_binary_signal(input_f, threshold=0.2)
    #     plot_binary_signal(binary_signal, sr=librosa.get_samplerate(input_f))
    #     if index == 2:
    #         break
    # input_f = "./ESC-50-master/ audio.wav"
    #
    # output_f = "path/to/your/output/audio_without_silence.wav"
    # remove_silence(input_f, output_f)

