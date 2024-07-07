from datetime import datetime
import tkinter as tk
import customtkinter
from tkinter import ttk
import threading
import time
from functools import partial

from Experiments.SessionHandler import SessionHandler
from Logger import Logger
from Setting import Settings
from NaturalAudioTDT import play_natural_stimulus_set, play_lf_tone
from TDTController.Global import TDTGlobal

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class ModernUIExample:
    def __init__(self, main_window):
        self.root = main_window
        self.settings = Settings()
        self.logger = Logger(f"software_logs//{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

        self.tdt = TDTGlobal()

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate window size
        window_width = screen_width // 2
        window_height = screen_height - 80

        self.root.title("Neuropixel Recording Software")
        self.root.geometry(f"{window_width}x{window_height}+0+0")  # Set the initial size of the window

        num_columns = 4
        num_rows = 17

        self.toggle_able_comps = []

        for col in range(num_columns):
            root.grid_columnconfigure(col, weight=1)

        for row in range(num_rows):
            root.grid_rowconfigure(row, weight=1)

        self.frames = {}
        for row in range(num_rows):
            for col in range(num_columns):
                frame = customtkinter.CTkFrame(self.root, corner_radius=0, bg_color="#242424", fg_color="#242424")
                frame.grid(row=row, column=col, sticky='nsew', padx=0, pady=1)
                self.frames[f"{row}-{col}"] = frame

        #
        heading = customtkinter.CTkLabel(master=self.root, text="Neuropixel Recording Software")
        heading.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=0, pady=1)
        # heading.grid(row=0, , sticky='nsew')

        brain_region_label = customtkinter.CTkLabel(master=self.root, text="Please select the electrode location:")
        brain_region_label.grid(row=1, column=0, columnspan=2, sticky="nsw", padx=20, pady=1)

        self.electrode_location = tk.StringVar()

        # Create a combobox and bind it to the StringVar
        electrode_location_combobox = customtkinter.CTkComboBox(self.root, values=["A1", "AAF", "PAF", "A2", "DZ"],
                                                                variable=self.electrode_location)
        electrode_location_combobox.grid(row=1, column=2, columnspan=2, padx=20, pady=10, sticky="nsew")

        self.toggle_able_comps.append(electrode_location_combobox)

        # Set the initial value (optional)
        self.electrode_location.set("A1")
        # Test the recording setup.
        test_buttons = ["Test with Pure Tones", "Test with White Noises", "Test with Natural Stimuli",
                        "Test with Ultrasonic Tones"]

        test_buttons_holder = {}

        test_recording_setup_label = customtkinter.CTkLabel(master=self.root,
                                                            text="Test the recording setup: The test may take around 2 minutes.")
        test_recording_setup_label.grid(row=2, column=0, columnspan=2, sticky="nsw", padx=20, pady=1)

        for i, tst_btn in enumerate(test_buttons):
            test_buttons_holder[i] = customtkinter.CTkButton(self.root, text=tst_btn,
                                                             command=partial(self.test_button_clicked,
                                                                             tst_btn.replace(" ", "_").lower()))
            test_buttons_holder[i].grid(row=3, column=i, sticky="nsew", padx=10, pady=10)

            self.toggle_able_comps.append(test_buttons_holder[i])

        session_based_recordings = ["Natural Stim", "Natural Stim Ext", "Ultrasonic Vocalization"]
        session_counts = [3, 2, 6]

        natural_sound_label = customtkinter.CTkLabel(master=self.root,
                                                     text="Natural Stimulation: Please select"
                                                          " the session and then click on start.")
        natural_sound_label.grid(row=5, column=0, columnspan=2, sticky="nsw", padx=20, pady=1)

        self.session_based_recording_holder = {}
        self.session_number_variables = {}
        self.max_session_count = {}
        for i, session_rec in enumerate(session_based_recordings):
            sec_id = session_rec.replace(" ", "_").lower()
            self.session_number_variables[sec_id] = tk.IntVar(value=0)
            self.max_session_count[sec_id] = session_counts[i]
            ui_holder = {}
            ui_holder['slider'] = self.ns_session_selector = customtkinter.CTkSlider(self.root, from_=0,
                                                                                     to=session_counts[i],
                                                                                     number_of_steps=
                                                                                     session_counts[i],
                                                                                     variable=
                                                                                     self.session_number_variables[
                                                                                         sec_id])

            ui_holder['slider'].grid(row=6 + i, column=0, columnspan=2, padx=10, pady=10, sticky="we")

            self.toggle_able_comps.append(ui_holder['slider'])

            ui_holder['text_display'] = customtkinter.CTkLabel(self.root, textvariable=self.session_number_variables[
                sec_id])
            ui_holder['text_display'].grid(row=6 + i, column=2, padx=10, pady=10, sticky="we")

            ui_holder['button'] = customtkinter.CTkButton(self.root, text=f"Start {session_rec}",
                                                          command=partial(self.start_session_btn, sec_id))

            ui_holder['button'].grid(row=6 + i, column=3, sticky="nsew", padx=10, pady=10)

            self.toggle_able_comps.append(ui_holder['button'])

            self.session_based_recording_holder[sec_id] = ui_holder

        # self.natural_stimulus_session = tk.IntVar(value=0)
        # # self.natural_stimulus_session.trace("w", self.update_ns_session_selector)
        #
        # self.ns_session_selector = customtkinter.CTkSlider(self.root, from_=0, to=3, number_of_steps=3,
        #                                                    # command=self.ns_session_selector_event,
        #                                                    variable=self.natural_stimulus_session)
        # self.ns_session_selector.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        #
        # self.toggle_able_comps.append(self.ns_session_selector)
        #
        # ns_session_selector_display = customtkinter.CTkLabel(self.root, textvariable=self.natural_stimulus_session)
        # ns_session_selector_display.grid(row=5, column=2, padx=10, pady=10, sticky="we")
        #
        # natural_stimulus_start_recording = customtkinter.CTkButton(self.root, text="Start Recording",
        #                                                            command=self.start_time_consuming_function)
        # natural_stimulus_start_recording.grid(row=5, column=3, sticky="nsew", padx=10, pady=10)
        #
        # self.toggle_able_comps.append(natural_stimulus_start_recording)
        #
        # # Natural Stimulus Extension Set:
        # natural_sound_ext_label = customtkinter.CTkLabel(master=self.root,
        #                                                  text="Natural Sound Stimulation Extension:")
        # natural_sound_ext_label.grid(row=6, column=0, columnspan=2, sticky="nsw", padx=20, pady=1)
        #
        # # Create an integer variable and bind it to the slider
        # self.natural_stimulus_ext_session = tk.IntVar(value=0)
        # # self.natural_stimulus_ext_session.trace("w", self.update_ns_ext_session_selector)
        #
        # # Create the slider bar with range 1 to 10 at the bottom
        # self.ns_ext_session_selector = customtkinter.CTkSlider(self.root, from_=0, to=3, number_of_steps=3,
        #                                                        # command=self.ns_ext_session_selector_event,
        #                                                        variable=self.natural_stimulus_ext_session)
        # self.ns_ext_session_selector.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        #
        # self.toggle_able_comps.append(self.ns_ext_session_selector)
        #
        # ns_ext_session_selector_display = customtkinter.CTkLabel(self.root,
        #                                                          textvariable=self.natural_stimulus_ext_session)
        # ns_ext_session_selector_display.grid(row=7, column=2, padx=10, pady=10, sticky="we")
        #
        # # Create the second button in the next row
        # natural_stimulus_ext_start_recording = customtkinter.CTkButton(self.root, text="Start Recording",
        #                                                                command=None)
        # natural_stimulus_ext_start_recording.grid(row=7, column=3, sticky="nsew", padx=10, pady=10)
        #
        # self.toggle_able_comps.append(natural_stimulus_ext_start_recording)
        #
        # # Ultrasonic Vocalization
        #
        # ultrasonic_vocal_label = customtkinter.CTkLabel(master=self.root,
        #                                                 text="Ultrasonic Vocalization")
        # ultrasonic_vocal_label.grid(row=8, column=0, columnspan=2, sticky="nsw", padx=20, pady=1)
        #
        # # Create an integer variable and bind it to the slider
        # self.ultrasonic_vocalization_session = tk.IntVar(value=0)
        #
        # # Create the slider bar with range 1 to 10 at the bottom
        # self.ultrasonic_session_selector = customtkinter.CTkSlider(self.root, from_=0, to=3, number_of_steps=3,
        #                                                            variable=self.ultrasonic_vocalization_session)
        # self.ultrasonic_session_selector.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        #
        # self.toggle_able_comps.append(self.ultrasonic_session_selector)
        #
        # ultrasonic_selector_display = customtkinter.CTkLabel(self.root,
        #                                                      textvariable=self.ultrasonic_vocalization_session)
        # ultrasonic_selector_display.grid(row=9, column=2, padx=10, pady=10, sticky="we")
        #
        # # Create the second button in the next row
        # ultrasonic_vocal_start_recording = customtkinter.CTkButton(self.root, text="Start Recording",
        #                                                            command=self.show_popup)
        # ultrasonic_vocal_start_recording.grid(row=9, column=3, sticky="nsew", padx=10, pady=10)
        #
        # self.toggle_able_comps.append(ultrasonic_vocal_start_recording)

        # Progress Bar and Status Bar
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = customtkinter.CTkProgressBar(self.root, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(row=14, column=0, columnspan=3, padx=10, pady=10, sticky="we")

        emergency_break = customtkinter.CTkButton(self.root, text="Emergency Break",
                                                  command=None, fg_color="#881122")
        emergency_break.grid(row=14, column=3, sticky="nsew", padx=10, pady=10)

        #
        # # Create a text box for logging below the slider
        self.status_bar = customtkinter.CTkLabel(self.root, text="")
        self.status_bar.grid(row=15, column=0, columnspan=3, pady=10, sticky="nsw", padx=20)

        # Software Logs
        # Create a textbox
        self.user_log_textbox = customtkinter.CTkTextbox(self.root, height=1)
        self.user_log_textbox.grid(row=16, column=0, columnspan=3, sticky='nsew', padx=10, pady=5)
        root.grid_rowconfigure(16, weight=1)
        # Create a button

        # Create a styled button
        user_log_append_btn = customtkinter.CTkButton(root, text="Append Log", command=self.user_log_append_click,
                                                      fg_color="#338811")
        user_log_append_btn.grid(row=16, column=3, sticky='nsew', padx=10, pady=10)
        root.grid_rowconfigure(16, weight=1)

        self.original_colors = {}

        #
        # self.toggle_able_comps = [self.natural_stim_btn, self.slider, self.pure_tones_btn, self.white_noise_btn]

    # Function to update the slider when the integer variable changes

    def user_log_append_click(self):
        text = self.user_log_textbox.get("1.0", tk.END).strip()  # Get text from the textbox
        self.logger.user(text)  # Log text with INFO level
        self.user_log_textbox.delete("1.0", tk.END)  # Clear the textbox

    def toggle_ui_state(self, state):
        for comp in self.toggle_able_comps:
            comp.configure(state=state)
            if state == "disabled":
                # Store the original color if not already stored
                if comp not in self.original_colors:
                    self.original_colors[comp] = comp.cget("fg_color")
                # Change color to gray
                comp.configure(fg_color="#111111")
            elif state == "normal":
                # Restore the original color
                if comp in self.original_colors:
                    comp.configure(fg_color=self.original_colors[comp])
            # comp['state'] = state

    # Time-consuming function
    # def time_consuming_function(self):
    #     self.toggle_ui_state('disabled')
    #     for i in range(101):
    #         time.sleep(0.1)  # Simulate work being done
    #         self.update_progress(i)
    #         self.write_log(i)
    #         self.root.update_idletasks()
    #     self.toggle_ui_state('normal')
    #     self.natural_stimulus_session.set(self.natural_stimulus_session.get() + 1)

    def test_button_clicked(self, button):
        self.show_popup(f"{button} button was clicked")
        session_handler = SessionHandler(self)
        threading.Thread(target=session_handler.run_session,
                         args=()).start()

    # Function to start the time-consuming function in a separate thread
    def start_session_btn(self, ses_id):
        self.show_popup(f"{self.session_number_variables[ses_id].get()} is going to run!")
        threading.Thread(target=play_natural_stimulus_set,
                         args=(self.session_number_variables[ses_id], ses_id, self)).start()

    def update_progress(self, percent):
        self.progress_bar.set(percent / 100)
        self.root.update_idletasks()

    def write_log(self, log_message):
        self.status_bar.configure(text=log_message)
        self.root.update_idletasks()

    def show_popup(self, message="Please make sure that ultrasonic switch is on!"):
        # Create a new Toplevel window
        popup = customtkinter.CTkToplevel(self.root)
        # self.root.geometry(f"{400}x{300}+0+0")
        popup.geometry(f"{400}x{300}+200+200")
        popup.title("Warning!")

        popup.transient(self.root)

        # Make the popup modal
        popup.grab_set()

        # Focus on the popup
        popup.focus()

        # Add a label with the message
        label = customtkinter.CTkLabel(popup, text=message)
        label.pack(pady=10)

        # Add an OK button to close the popup
        ok_button = customtkinter.CTkButton(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        self.root.wait_window(popup)

    def on_closing(self):
        self.logger.info("Software Closed.")
        self.logger.close()
        self.root.destroy()

    def increment_session_number(self, ses_type):
        var = self.session_number_variables[ses_type]
        current_value = var.get()
        if current_value < self.max_session_count[ses_type]:
            var.set(current_value + 1)

    # Function to append text with timestamp to the file


# Create the main window and run the application
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = ModernUIExample(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
