import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, filtfilt, iirnotch


# Generate synthetic neural activity data with gamma oscillations
# np.random.seed(0)
# sampling_freq = 1000  # Hz
# t = np.arange(0, 10, 1 / sampling_freq)  # 10 seconds of data
# background_activity = 0.5 * np.sin(2 * np.pi * 5 * t)  # Low-frequency background activity
# gamma_activity = 0.2 * np.sin(2 * np.pi * 60 * t)  # Gamma oscillations at 60 Hz
# neural_data = background_activity + gamma_activity
#
# # Plot the original neural activity data
# plt.figure(figsize=(10, 4))
# plt.plot(t, neural_data, label='Original Neural Activity')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.title('Original Neural Activity Data')
# plt.legend()
# plt.grid(True)
# plt.show()
#
# # Define frequency range for gamma oscillations (e.g., 30-100 Hz)
# gamma_lowcut = 30.0
# gamma_highcut = 100.0


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def remove_gamma_band(neural_data, gamma_lowcut=30.0, gamma_highcut=200.0, sampling_freq=1000):
    # Apply bandpass filter to isolate gamma band
    gamma_band_data = butter_bandpass_filter(neural_data, gamma_lowcut, gamma_highcut, sampling_freq)

    # Compute the analytic signal using Hilbert transform
    analytic_signal = hilbert(gamma_band_data)

    # Extract instantaneous phase and amplitude
    instantaneous_phase = np.angle(analytic_signal)
    instantaneous_amplitude = np.abs(analytic_signal)

    # Manipulate the analytic signal to remove gamma band
    threshold = 0.15  # Adjust as needed
    instantaneous_amplitude[instantaneous_amplitude > threshold] = threshold

    # Reconstruct the modified analytic signal
    modified_analytic_signal = instantaneous_amplitude * np.exp(1j * instantaneous_phase)

    # Inverse Hilbert transform to obtain the modified neural activity data
    modified_neural_data = np.real(modified_analytic_signal)

    # return modified_neural_data
    return instantaneous_amplitude


def notch_filter(data, f0, fs):
    q = 30.0  # Quality factor
    b, a = iirnotch(f0, q, fs)
    y = filtfilt(b, a, data)
    return y

# # Apply bandpass filter to isolate gamma band
# gamma_band_data = butter_bandpass_filter(neural_data, gamma_lowcut, gamma_highcut, sampling_freq)
#
# # Compute the analytic signal using Hilbert transform
# analytic_signal = hilbert(gamma_band_data)
#
# # Extract instantaneous phase and amplitude
# instantaneous_phase = np.angle(analytic_signal)
# instantaneous_amplitude = np.abs(analytic_signal)
#
# # Manipulate the analytic signal to remove gamma band
# threshold = 0.15  # Adjust as needed
# instantaneous_amplitude[instantaneous_amplitude > threshold] = threshold
#
# # Reconstruct the modified analytic signal
# modified_analytic_signal = instantaneous_amplitude * np.exp(1j * instantaneous_phase)
#
# # Inverse Hilbert transform to obtain the modified neural activity data
# modified_neural_data = np.real(modified_analytic_signal)

# Plot the original and modified neural activity data
# plt.figure(figsize=(10, 6))
# plt.subplot(2, 1, 1)
# plt.plot(t, neural_data, label='Original Neural Activity')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.title('Original vs Modified Neural Activity Data')
# plt.legend()
# plt.grid(True)
#
# plt.subplot(2, 1, 2)
# plt.plot(t, modified_neural_data[:500], label='Modified Neural Activity')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.legend()
# plt.grid(True)
#
# plt.tight_layout()
# plt.show()
