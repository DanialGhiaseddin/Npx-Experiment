import os
import librosa
import soundfile as sf


def resample_audio_files(input_folder, output_folder, target_sr=24414):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load the audio file
            y, sr = librosa.load(input_path, sr=None)

            # Resample the audio
            y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)

            # Save the resampled audio file
            sf.write(output_path, y_resampled, target_sr)
            print(f"Resampled {filename} from {sr} Hz to {target_sr} Hz")


# Example usage
input_folder = './ESC-50-master/audio'  # Replace with your input folder path
output_folder = './ESC-50-master/audio_24414'  # Replace with your output folder path
resample_audio_files(input_folder, output_folder, target_sr=24414)
