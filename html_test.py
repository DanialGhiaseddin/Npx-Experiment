import tkinter as tk
from tkinter import simpledialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import numpy as np


def get_channels():
    # root = tk.Tk()
    # root.withdraw()
    channels = simpledialog.askstring("Input", "Enter comma-separated channel names (e.g., Channel 1, Channel 2):")
    return channels.split(',')


selected_channels = get_channels()

# Set up the Tkinter window
root = tk.Tk()
root.title("Interactive Plot with Tkinter")

# Create a figure and axis for the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Set the x and y axis to some dummy data
t = np.arange(0.0, 1.0, 0.001)
a0 = 6
f0 = 3
s = a0 * np.sin(2 * np.pi * f0 * t)

# Plot the initial data
plot, = ax.plot(t, s, lw=3, color='green')
ax.axis([0, 1, -10, 10])

# Set the Slider color
axcolor = "white"

# Set the frequency and amplitude axis
frequency_axis = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
amplitude_axis = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

# Set the slider for frequency and amplitude
frequency_slider = Slider(frequency_axis, 'Freq', 0.1, 30.0, valinit=f0)
amplitude_slider = Slider(amplitude_axis, 'Amp', 0.1, 10.0, valinit=a0)


# Update function to change the graph when the slider is in use
def update(val):
    amp = amplitude_slider.val
    freq = frequency_slider.val
    plot.set_ydata(amp * np.sin(2 * np.pi * freq * t))
    fig.canvas.draw_idle()


# Attach the update function to the sliders
frequency_slider.on_changed(update)
amplitude_slider.on_changed(update)

# Embed the matplotlib plot into the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a toolbar if needed (optional)
toolbar = tk.Frame(root)
toolbar.pack(side=tk.BOTTOM, padx=5, pady=5)
toolbar_btn = tk.Button(toolbar, text="Quit", command=root.destroy)
toolbar_btn.pack(side=tk.RIGHT)

# Run the Tkinter event loop
root.mainloop()
