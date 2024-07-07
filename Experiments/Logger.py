import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Logger:
    def __init__(self, filename=None):
        if filename is None:
            self.filename = f"software_logs//{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        else:
            self.filename = filename
        self.file = open(self.filename, "a")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file.write(f"{timestamp} - *** Software started ***\n")
        self.file.flush()

    def log(self, text, level="INFO"):
        if text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.file.write(f"{timestamp} - {level} - {text}\n")
            self.file.flush()

    def info(self, text):
        self.log(text, level="INFO")

    def recording(self, text):
        self.log(text, level="RECORDING")

    def user(self, text):
        self.log(text, level="USER")

    def warning(self, text):
        self.log(text, level="WARNING")

    def error(self, text):
        self.log(text, level="ERROR")

    def close(self):
        self.file.close()


if __name__ == "__main__":
    # Function to handle button click
    pass
