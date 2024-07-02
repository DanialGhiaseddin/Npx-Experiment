import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Generate some random multichannel time series data
np.random.seed(42)
num_channels = 5
num_samples = 1000

data = {
    'Time': np.arange(num_samples),
}

for i in range(num_channels):
    data[f'Channel {i+1}'] = np.random.randn(num_samples)

df = pd.DataFrame(data)

# Create subplots with shared x-axis
fig = make_subplots(rows=num_channels, cols=1, shared_xaxes=True, subplot_titles=df.columns[1:])

# Add traces for each channel
for i, col in enumerate(df.columns[1:]):
    fig.add_trace(go.Scatter(x=df['Time'], y=df[col], mode='lines', name=f'{col}'), row=i + 1, col=1)

# Update layout for better readability
fig.update_layout(title='Multichannel Time Series', showlegend=False)

# Add horizontal scroll functionality
fig.update_xaxes(rangeslider_visible=True)

# Show the plot
fig.show()
