import tkinter
import tkinter.messagebox
from os import path
from tkinter import filedialog
import customtkinter
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import tdt
from pygame import mixer
import pandas as pd

from Analyzing.signal.processing import relative_crop, normalization, resample_by_interpolation
from Analyzing.GraphicalInterface.utils.log import parse_log_file, find_log_files

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.directory = filedialog.askdirectory(initialdir=".",
                                                 title='Please select signal(s) from the list.')

        self.tdt_data = tdt.read_block(self.directory)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=0, rowspan=4, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Stimulation Viewer")
        self.tabview.tab("Stimulation Viewer").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Stimulation Viewer").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        self.stimulation_viewer_page = StimulusViewerPage(tdt_directory=self.directory, tdt_data=self.tdt_data,
                                                          master=self.tabview.tab("Stimulation Viewer"))
        self.stimulation_viewer_page.grid(row=0, column=0, padx=0, pady=0, rowspan=4, columnspan=2, sticky="nsew")


class StimulusViewerPage(customtkinter.CTkFrame):
    def __init__(self, tdt_directory, tdt_data, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.tdt_directory = tdt_directory
        self.tdt_data = tdt_data

        self.audio_set_directory = ('/home/danial/Documents/Projects/McGill/Npx-Experiment/Stimulus '
                                    'Preprocessing/ESC-50-master/audio_test/')

        self.esc50_df = pd.read_csv(
            '/Stimulus Preprocessing/ESC-50-master/meta/esc50.csv')

        log_file = find_log_files(self.tdt_directory)[0]
        _, self.stim_orders = parse_log_file(log_file)

        self.onsets = self.tdt_data['epocs'].Tr1_.onset
        self.offsets = self.tdt_data['epocs'].Tr1_.offset

        self.audio_file_name = tkinter.StringVar()
        self.audio_file_category = tkinter.StringVar()

        mixer.init()
        with (open(path.join(self.tdt_directory, 'TDT_Presentation.csv')) as f):
            self.played_stimuli = f.readlines()[0].split(',')
        self.played_stimuli = [stimulus.split('||')[0] for stimulus in self.played_stimuli]
        self.index_to_name_map = {}
        self.name_to_index_map = {}
        for i, stimulus in enumerate(self.played_stimuli):
            self.index_to_name_map[i + 1] = stimulus
            self.name_to_index_map[stimulus] = i + 1

        self.disp_stim_index = 0
        self.selected_trial = 0

        self._create_widgets()

        self._update()

    def _create_widgets(self):
        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        # self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(4, weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0, border_width=5)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="TDT Recoding Viewer",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"))
        self.logo_label.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(10, 20))

        self.signal_filtering_btn = customtkinter.CTkButton(self.sidebar_frame, text="Signal Filtering")
        self.signal_filtering_btn.grid(row=1, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")

        self.open_in_browser = customtkinter.CTkButton(self.sidebar_frame, text="Open in Browser", command=self.plot)
        self.open_in_browser.grid(row=2, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")

        # self.plot_frame = customtkinter.CTkFrame(self, corner_radius=0, border_width=1, fg_color="red")
        # self.plot_frame.grid(row=0, column=1, sticky="nsew")

        self.control_frame = customtkinter.CTkFrame(self, corner_radius=0, height=50, border_width=1)
        self.control_frame.grid(row=4, column=1, sticky="nsew")
        self.control_frame.grid_rowconfigure((0, 1), weight=1)
        self.control_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Arrange the control frame in the bottom row of software
        self.stim_class_label = None
        self.stim_file_label = None

        # self.grid_columnconfigure(4, weight=1)

        button = customtkinter.CTkButton(self.control_frame, text='Play', command=self.play_audio)
        button.grid(pady=0, padx=5, row=0, column=0)

        self.combobox_1 = customtkinter.CTkComboBox(self.control_frame,
                                                    values=self.played_stimuli, command=self.callback)
        self.combobox_1.grid(row=1, column=0, padx=5, pady=(0, 0))
        self.combobox_1.bind("<<ComboboxSelected>>", self.callback)

        # combobox_1.bind("<<ComboboxSelected>>", self.callback)

        stim_file_head = customtkinter.CTkLabel(self.control_frame, text="Stimulus File")
        stim_file_head.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")
        self.stim_file_label = customtkinter.CTkLabel(self.control_frame, textvariable=self.audio_file_name)
        self.stim_file_label.grid(row=0, column=2, pady=5, padx=5, sticky="nsew")

        stim_class_head = customtkinter.CTkLabel(self.control_frame, text="Stimulus Category:")
        stim_class_head.grid(row=1, column=1, pady=5, padx=5, sticky="nsew")
        self.stim_class_label = customtkinter.CTkLabel(self.control_frame, textvariable=self.audio_file_category)
        self.stim_class_label.grid(row=1, column=2, pady=5, padx=5, sticky="nsew")

        next_button = customtkinter.CTkButton(self.control_frame, text='Next', command=self.change_to_next_stimulus)
        next_button.grid(pady=0, padx=5, row=0, column=3)

        prv_button = customtkinter.CTkButton(self.control_frame, text='Previous', command=self.change_to_prev_stimulus)
        prv_button.grid(pady=0, padx=5, row=1, column=3)
        # self.audio_player_app = StimulusControlFrame(self.control_frame)
        # self.audio_player_app.grid(row=0, column=0, sticky="nsew")
        self.trial_combo = customtkinter.CTkComboBox(self.control_frame,
                                                     values=[str(i) for i in range(5)],
                                                     command=self.trial_combo_callback)
        self.trial_combo.grid(row=1, column=4, padx=5, pady=(0, 0))
        self.trial_combo.bind("<<ComboboxSelected>>", self.trial_combo_callback)

    def plot(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)
        fig.patch.set_facecolor('#2b2b2b')

        raw_data = []
        sample_rates = []
        signal_names_list = ['RSTM','RSYN','LFPR']

        # Filter desired signals for plotting

        for signal_name in signal_names_list:
            raw_data.append(self.tdt_data['streams'][signal_name]['data'])
            sample_rates.append(float(self.tdt_data['streams'][signal_name]['fs']))

        # Resample signals to 3000 Hz
        for i, raw_data_sig in enumerate(raw_data):
            if len(raw_data_sig.shape) > 1:
                n_sig = []
                for c in range(min(raw_data_sig.shape[0], 8)):
                    n_sig.append(resample_by_interpolation(raw_data_sig[c], sample_rates[i], 3000))
                raw_data[i] = np.vstack(n_sig)
            else:
                raw_data[i] = resample_by_interpolation(raw_data_sig, sample_rates[i], 3000).reshape(1, -1)

        plot_channels = 0
        for raw_data_sig in raw_data:
            plot_channels += min(raw_data_sig.shape[0], 8)

        exp_duration = self.tdt_data['info']['duration']
        exp_duration = float(f"{exp_duration.seconds}.{exp_duration.microseconds}")

        start_indices = [(onset - 0.5) / exp_duration for onset in self.selected_onsets] # [self.selected_trial]
        end_indices = [(onset + 5.5) / exp_duration for onset in self.selected_onsets] # [self.selected_trial]
        average = True
        plot_index = 0
        for i, raw_data_sig in enumerate(raw_data):
            for c in range(min(raw_data_sig.shape[0], 8)):
                plot = fig.add_subplot(plot_channels, 1, plot_index + 1)
                avg_signal = None
                for trial in range(len(start_indices)):
                    f_signal = relative_crop(raw_data_sig[c], start_indices[trial], end_indices[trial])
                    f_signal = normalization(f_signal)
                    if avg_signal is None:
                        avg_signal = np.zeros((len(start_indices), f_signal.shape[-1] + 10))
                    avg_signal[trial] = np.pad(f_signal, (0, avg_signal.shape[-1] - f_signal.shape[-1]), 'constant')
                    if not average:
                        plot.plot(f_signal)
                if average:
                    plot.plot(np.mean(avg_signal, axis=0))
                fig.gca().set_axis_off()
                plot_index += 1

        # list of squares
        # x = np.arange(0, 100, 0.1)

        # num_subplots = 20
        # for i in range(num_subplots):
        # Add a subplot to the figure
        # plot = fig.add_subplot(num_subplots, 1, i + 1)

        # y = np.random.rand(len(x))
        # Plot the graph on each subplot
        # plot.plot(x, y, label=f'Subplot {i + 1}')
        # plot.legend(loc='center left')
        # fig.gca().set_axis_off()

        fig.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)

        canvas = FigureCanvasTkAgg(fig,
                                   master=self)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=4, sticky="nsew")

    def _update(self):
        stim_file = self.played_stimuli[self.disp_stim_index]

        self.audio_file_name.set(stim_file)

        self.audio_file_path = path.join(self.audio_set_directory, stim_file)

        self.audio_file_category.set(
            self.esc50_df.loc[self.esc50_df['filename'] == stim_file, 'category'].values[0])

        selected_trials = self.find_trials(stim_file)

        self.selected_onsets = self.onsets[selected_trials]
        self.selected_offsets = self.offsets[selected_trials]
        self.plot()

    def find_trials(self, stim_name):
        idx = self.name_to_index_map[stim_name]
        trials = []
        for i, stim_log in enumerate(self.stim_orders):
            if f"F-{idx}" == stim_log:
                trials.append(i)
        return trials

    def play_audio(self):
        # Stop any currently playing audio
        mixer.music.stop()

        # Load and play the selected audio file
        mixer.music.load(self.audio_file_path)
        mixer.music.play()

    def change_to_next_stimulus(self):
        if self.disp_stim_index < len(self.played_stimuli) - 1:
            self.disp_stim_index += 1
            self._update()

    def change_to_prev_stimulus(self):
        if self.disp_stim_index > 0:
            self.disp_stim_index -= 1
            self._update()

    def callback(self, event):
        self.disp_stim_index = self.name_to_index_map[self.combobox_1.get()] - 1
        print(self.disp_stim_index)
        self._update()

    def trial_combo_callback(self, event):
        self.selected_trial = int(self.trial_combo.get())
        self._update()


if __name__ == "__main__":
    app = App()
    app.mainloop()
