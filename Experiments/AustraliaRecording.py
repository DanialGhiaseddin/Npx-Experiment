from datetime import datetime
import tkinter as tk
from tkinter import ttk
import threading
import time

from Logger import Logger
from Setting import Settings
from NaturalAudioTDT import play_natural_stimulus_set


class ModernUIExample:
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        self.logger = Logger(f"software_logs//{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate window size
        window_width = screen_width // 2
        window_height = screen_height - 80

        self.root.title("Neuropixel Recording Software")
        self.root.geometry(f"{window_width}x{window_height}+0+0")  # Set the initial size of the window

        num_columns = 4
        num_rows = 15

        for col in range(num_columns):
            root.grid_columnconfigure(col, weight=1)

        for row in range(num_rows):
            root.grid_rowconfigure(row, weight=1)

        # Add frames to demonstrate the grid layout
        for row in range(num_rows):
            for col in range(num_columns):
                frame = tk.Frame(root, bg=f'#000088', padx=1, pady=1)
                frame.grid(row=row, column=col, sticky='nsew')
                label = tk.Label(frame, text=f"Row {row + 1}, Col {col + 1}")
                label.pack(expand=True, fill=tk.BOTH)

        #
        heading = tk.Label(self.root, text="Neuropixel Recording Software")
        heading.grid(row=0, columnspan=4, sticky='nsew')

        # Software Logs
        # Create a textbox
        self.user_log_textbox = tk.Text(self.root, height=0.5)
        self.user_log_textbox.grid(row=14, column=0, columnspan=3, sticky='nsew', padx=10, pady=5)
        root.grid_rowconfigure(14, weight=1)
        # Create a button

        # Create a styled button
        user_log_append_btn = ttk.Button(root, text="Append Log", command=self.user_log_append_click)
        user_log_append_btn.grid(row=14, column=3, sticky='nsew', padx=10, pady=20)
        root.grid_rowconfigure(14, weight=1)

        # # Configure the style for modern look
        # style = ttk.Style()
        # style.configure("TButton", font=("Helvetica", 12), padding=10)
        # style.configure("TScale", font=("Helvetica", 12))
        # style.configure("TProgressbar", thickness=20)
        #
        # # Make the window resizable
        # self.root.resizable(True, True)
        #
        # # Create the first button on the left
        # self.natural_stim_btn = ttk.Button(self.root, text="Play Natural Stimulus",
        #                                    command=self.start_time_consuming_function)
        # self.natural_stim_btn.grid(row=0, column=0, columnspan=2, padx=140, pady=10, sticky="we")
        #
        # # Create an integer variable and bind it to the slider
        # self.stimulus_set = tk.IntVar(value=1)
        # self.stimulus_set.trace("w", self.update_slider)
        #
        # # Create the slider bar with range 1 to 10 at the bottom
        # self.slider = ttk.Scale(self.root, from_=1, to=3, orient="horizontal", command=self.update_value_from_slider)
        # self.slider.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        #
        # self.slider_display = tk.Entry(self.root, textvariable=self.stimulus_set, state='readonly', width=5)
        # self.slider_display.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        #
        # # Create the second button in the next row
        # self.pure_tones_btn = ttk.Button(self.root, text="Play Pure Tones")
        # self.pure_tones_btn.grid(row=2, column=0, columnspan=2, padx=140, pady=10, sticky="we")
        #
        # # Create the third button in the next row
        # self.white_noise_btn = ttk.Button(self.root, text="Play White Noise")
        # self.white_noise_btn.grid(row=3, column=0, columnspan=2, padx=140, pady=10, sticky="we")
        #
        # # Create a progress bar at the end of the page
        # self.progress_bar = ttk.Progressbar(self.root, mode='determinate', maximum=100)
        # self.progress_bar.grid(row=4, column=0, padx=10, pady=10, sticky="we")
        #
        # # Create a text box for logging below the slider
        # self.log_text = tk.Text(self.root, height=4)
        # self.log_text.grid(row=5, column=0,columnspan=2, padx=10, pady=10, sticky="we")
        #
        # self.toggle_able_comps = [self.natural_stim_btn, self.slider, self.pure_tones_btn, self.white_noise_btn]
        #
        # # Configure the grid to allow the slider and progress bar to expand horizontally
        # # Configure the grid to allow the slider, log text box, and progress bar to expand horizontally
        # self.root.grid_columnconfigure(0, weight=8)
        # self.root.grid_columnconfigure(1, weight=1)

    # Function to update the slider when the integer variable changes

    def user_log_append_click(self):
        text = self.user_log_textbox.get("1.0", tk.END).strip()  # Get text from the textbox
        self.logger.user(text)  # Log text with INFO level
        self.user_log_textbox.delete("1.0", tk.END)  # Clear the textbox

    def update_slider(self, *args):
        self.slider.set(self.stimulus_set.get())

    # Function to update the integer variable when the slider moves
    def update_value_from_slider(self, value):
        self.stimulus_set.set(int(float(value)))

    def toggle_ui_state(self, state):
        for comp in self.toggle_able_comps:
            comp['state'] = state

    # Time-consuming function
    def time_consuming_function(self):
        self.toggle_ui_state('disabled')
        for i in range(101):
            time.sleep(0.1)  # Simulate work being done
            self.update_progress(i)
            self.write_log(i)
            self.root.update_idletasks()
        self.toggle_ui_state('normal')
        self.stimulus_set.set(self.stimulus_set.get() + 1)

    # Function to start the time-consuming function in a separate thread
    def start_time_consuming_function(self):

        threading.Thread(target=play_natural_stimulus_set, args=(self.stimulus_set.get(), self)).start()

    def update_progress(self, percent):
        self.progress_bar['value'] = percent
        self.root.update_idletasks()

    def write_log(self, log_message):
        self.log_text.delete(1.0, tk.END)  # Clear previous log
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def on_closing(self):
        self.logger.info("Software Closed.")
        self.logger.close()
        self.root.destroy()

    # Function to append text with timestamp to the file
    def append_text():
        text = text_box.get("1.0", tk.END).strip()  # Get text from the textbox
        if text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("output.txt", "a") as file:
                file.write(f"{timestamp} - {text}\n")  # Append timestamp and text to the file
            text_box.delete("1.0", tk.END)  # Clear the textbox


# Create the main window and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernUIExample(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
