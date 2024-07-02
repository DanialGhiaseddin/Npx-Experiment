import pandas as pd
import os

# Assuming you have a DataFrame called 'df' with a column 'filename'
# Example DataFrame
df = pd.read_csv("./ESC-50-master/meta/esc50.csv")

# Path to the directory containing the files
directory_path = './ESC-50-master/audio_test'

# Iterate through DataFrame rows
for index, row in df.iterrows():
    file_path = os.path.join(directory_path, row['filename'])

    # Check if the file exists
    if not os.path.exists(file_path):
        # Remove the row if the file is missing
        df.drop(index, inplace=True)

# Reset the index if needed
df.reset_index(drop=True, inplace=True)

# Display the updated DataFrame
print(df['category'].unique())
