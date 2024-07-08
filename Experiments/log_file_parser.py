import os


# Function to read the log file and extract the path, FSet value, list of ids, and start recording time for all sections
def extract_info_from_log(file_path):
    sections = []
    current_section = {'step': None, 'path': None, 'experiment': None, 'ids': [], 'start_recording_time': None}

    with open(file_path, 'r') as file:
        for line in file:
            if "INFO - Step " in line and "is done" in line:
                sections.append(current_section)
                current_section = {'step': None, 'path': None, 'experiment': None, 'ids': [],
                                   'start_recording_time': None}
            elif "INFO - Step " in line and "is starting" in line:
                if current_section['step'] is not None:
                    sections.append(current_section)
                    current_section = {'step': None, 'path': None, 'experiment': None, 'ids': [],
                                       'start_recording_time': None}
                current_section['step'] = line.split("INFO - ")[1].split(" is starting")[0].strip()
            elif "Data will be saved to" in line:
                current_section['path'] = line.split("Data will be saved to ")[1].strip()
            elif "TDT experiment switched to" in line:
                current_section['experiment'] = line.split("TDT experiment switched to ")[1].strip()
            elif "Playing:" in line:
                id_part = line.split("Playing: ")[1]
                id_value = int(id_part.split("id': ")[1].strip().strip("}"))
                current_section['ids'].append(id_value)
            elif "INFO - Starting TDT recording" in line:
                current_section['start_recording_time'] = line.split(" - INFO - Starting TDT recording...")[0].strip()

    if current_section['step'] is not None:
        sections.append(current_section)

    for i, s in enumerate(sections):
        s['tdt_path'] = os.path.join(s['path'],find_matching_folder(s['path'], s['start_recording_time']))

    return sections


def find_matching_folder(base_path, start_recording_time):
    # Convert the start recording time to match the folder format (e.g., "240707-214359")
    formatted_time = start_recording_time.replace("-", "").replace(":", "").replace(" ", "-")[2:]

    for folder_name in os.listdir(base_path):
        if formatted_time in folder_name:
            return folder_name

    return None


if __name__ == '__main__':
    # Example usage
    log_file_path = 'C:/Users/Lomber/Desktop/Npx-Experiment/Experiments/session_logs/20240708_011901_natural_stimuli_0.log'
    extracted_sections = extract_info_from_log(log_file_path)

    for index, section in enumerate(extracted_sections):
        print(f"Section {index + 1}:")
        print("Step:", section['step'])
        print("Extracted Path:", section['path'])
        print("FSet Value:", section['experiment'])
        print("Start Recording Time:", section['start_recording_time'])
        print("List of IDs:", section['ids'])
        print()
