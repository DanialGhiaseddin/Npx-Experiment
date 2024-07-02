from tkinter import IntVar
from typing import Union, Tuple, Optional

import math

from customtkinter import CTkCheckBox
from customtkinter.windows.widgets import CTkLabel
from customtkinter.windows.widgets import CTkEntry
from customtkinter.windows.widgets import CTkButton
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter.windows.widgets.font import CTkFont


class ChannelSelectionDialog(CTkToplevel):
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 checkbox_items: Optional[list] = None,  # Add a new parameter for checkbox items
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 title: str = "CTkDialog",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 text: str = "CTkDialog"):

        self._checkbox_items = checkbox_items

        super().__init__(fg_color=fg_color)

        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._text_color = ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else self._check_color_type(button_hover_color)
        self._button_fg_color = ThemeManager.theme["CTkButton"]["fg_color"] if button_fg_color is None else self._check_color_type(button_fg_color)
        self._button_hover_color = ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._button_text_color = ThemeManager.theme["CTkButton"]["text_color"] if button_text_color is None else self._check_color_type(button_text_color)
        self._entry_fg_color = ThemeManager.theme["CTkEntry"]["fg_color"] if entry_fg_color is None else self._check_color_type(entry_fg_color)
        self._entry_border_color = ThemeManager.theme["CTkEntry"]["border_color"] if entry_border_color is None else self._check_color_type(entry_border_color)
        self._entry_text_color = ThemeManager.theme["CTkEntry"]["text_color"] if entry_text_color is None else self._check_color_type(entry_text_color)

        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._title = title
        self._text = text
        self._font = font

        self.title(self._title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10, self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

    def _create_widgets(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure((0,), weight=1)

        self._label = CTkLabel(master=self,
                               width=300,
                               wraplength=300,
                               fg_color="transparent",
                               text_color=self._text_color,
                               text=self._text,
                               font=self._font)

        num_of_columns = math.ceil(len(self._checkbox_items) / 10)

        self._label.grid(row=1, column=0, columnspan=num_of_columns, padx=20, pady=20, sticky="ew")

        # self._entry = CTkEntry(master=self,
        #                        width=230,
        #                        fg_color=self._entry_fg_color,
        #                        border_color=self._entry_border_color,
        #                        text_color=self._entry_text_color,
        #                        font=self._font)
        # self._entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        col_index = 0

        if self._checkbox_items:
            self.checkboxes = []
            for idx, (checkbox_text, initial_value) in enumerate(self._checkbox_items):
                checkbox_var = IntVar(value=initial_value)
                checkbox = CTkCheckBox(
                    master=self,
                    text=checkbox_text,
                    variable=checkbox_var,
                    onvalue=1, offvalue=0
                )
                checkbox.grid(row=(idx%10) + 2, column=math.floor(idx/10), columnspan=2, padx=50, pady=(0, 30), sticky="w")
                self.checkboxes.append((checkbox_var, checkbox_text))

        self._ok_button = CTkButton(master=self,
                                    width=100,
                                    border_width=0,
                                    fg_color=self._button_fg_color,
                                    hover_color=self._button_hover_color,
                                    text_color=self._button_text_color,
                                    text='Ok',
                                    font=self._font,
                                    command=self._ok_event)
        self._ok_button.grid(row=len(self._checkbox_items) + 2, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew")

        self._cancel_button = CTkButton(master=self,
                                        width=100,
                                        border_width=0,
                                        fg_color=self._button_fg_color,
                                        hover_color=self._button_hover_color,
                                        text_color=self._button_text_color,
                                        text='Cancel',
                                        font=self._font,
                                        command=self._cancel_event)
        self._cancel_button.grid(row=len(self._checkbox_items) + 2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew")

        # self.after(150, lambda: self._entry.focus())  # set focus to entry with slight delay, otherwise it won't work
        # self._entry.bind("<Return>", self._ok_event)

    def _ok_event(self, event=None):
        checkbox_results = [(text, var.get()) for var, text in self.checkboxes]
        print(checkbox_results)
        self._user_input = checkbox_results
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input
