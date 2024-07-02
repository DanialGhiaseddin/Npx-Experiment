import os
import re


def parse_log_file(file_path):
    log_entries = []
    stim_orders = []
    log_entry_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} (\d{2}:\d{2}:\d{2})) - Stimulus presented - (\w+-\d+)')

    with open(file_path, 'r') as file:
        for line in file:
            match = log_entry_pattern.match(line)
            if match:
                timestamp, time, stimulus = match.groups()
                result = {'time': time, 'stimulus': stimulus}
                log_entries.append(result)
                stim_orders.append(stimulus)

    return log_entries, stim_orders


def find_log_files(directory):
    log_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            log_files.append(os.path.join(directory, filename))
    return log_files


if __name__ == '__main__':
    # Replace 'your_log_file.txt' with the actual path to your log file
    log_file_path = '/Analyzing/data/tdt tanks/Subject1-231219-150250/stimulus_log_20231219_150250.log'
    parsed_log_entries, stim_orders = parse_log_file(log_file_path)

    # Now 'parsed_log_entries' is a list of dictionaries, where each dictionary represents a log entry
    for entry in parsed_log_entries:
        print(entry)
