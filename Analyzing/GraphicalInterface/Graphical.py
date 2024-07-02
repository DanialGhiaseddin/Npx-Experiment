import tkinter as tk
from tkinter import simpledialog
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Function to get user input for channels
def get_channels():
    root = tk.Tk()
    root.withdraw()
    channels = simpledialog.askstring("Input", "Enter comma-separated channel names (e.g., Channel 1, Channel 2):")
    return channels.split(',')

# Generate some random multichannel time series data
np.random.seed(42)
num_channels = 5
num_samples = 1000

data = {'Time': np.arange(num_samples)}
for i in range(num_channels):
    data[f'Channel {i+1}'] = np.random.randn(num_samples)

df = pd.DataFrame(data)

# Get user input for channels
selected_channels = get_channels()

# Filter DataFrame based on selected channels
selected_df = df[['Time'] + selected_channels]

# Create subplots with shared x-axis
fig = make_subplots(rows=len(selected_channels), cols=1, shared_xaxes=True, subplot_titles=selected_channels)

# Add traces for each selected channel
for i, col in enumerate(selected_channels):
    fig.add_trace(go.Scatter(x=selected_df['Time'], y=selected_df[col], mode='lines', name=f'{col}'), row=i + 1, col=1)

# Update layout for better readability
fig.update_layout(title='Multichannel Time Series', showlegend=False)

# Add horizontal scroll functionality
fig.update_xaxes(rangeslider_visible=True)

# Show the plot
fig.show()
