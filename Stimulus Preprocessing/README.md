* This File Contains the code for the preprocessing of the stimulus data. 
* The stimulus data are audio files that are collected form ESC-50 dataset.
* The audio files will be played using TDT device and the response will be recorded using the same device.
  * The preprocessing step contains:
    * Silence Removal
    * dB Scaling and normalization
    * Time Matching
    * Finding max frequency
    * Quality Check
* How To Use:
* 1. Download the ESC-50 dataset from the link:
* 2. Extract the audio files from the dataset and place them in the folder named "audio_files".