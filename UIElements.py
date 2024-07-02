from typing import Optional, Union, Tuple
from customtkinter.windows.widgets import CTkLabel, CTkEntry, CTkButton, CTkCheckBox  # Import the necessary widgets
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter.windows.widgets.font import CTkFont

from tkinter import IntVar


class CTkCheckBoxDialog(CTkToplevel):
    def __init__(
            self,
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
            text: str = "CTkDialog",
    ):
        super().__init__(fg_color=fg_color)

        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(
            fg_color)
        self._text_color = ThemeManager.theme["CTkLabel"][
            "text_color"] if text_color is None else self._check_color_type(button_hover_color)
        self._button_fg_color = ThemeManager.theme["CTkButton"][
            "fg_color"] if button_fg_color is None else self._check_color_type(button_fg_color)
        self._button_hover_color = ThemeManager.theme["CTkButton"][
            "hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._button_text_color = ThemeManager.theme["CTkButton"][
            "text_color"] if button_text_color is None else self._check_color_type(button_text_color)
        self._entry_fg_color = ThemeManager.theme["CTkEntry"][
            "fg_color"] if entry_fg_color is None else self._check_color_type(entry_fg_color)
        self._entry_border_color = ThemeManager.theme["CTkEntry"][
            "border_color"] if entry_border_color is None else self._check_color_type(entry_border_color)
        self._entry_text_color = ThemeManager.theme["CTkEntry"][
            "text_color"] if entry_text_color is None else self._check_color_type(entry_text_color)

        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._title = title
        self._text = text
        self._font = font

        self.title(self._title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10,
                   self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

        self._checkbox_items = checkbox_items

    def _create_widgets(self):
        # ... (existing code remains the same)

        # Create checkboxes dynamically
        if self._checkbox_items:
            self.checkboxes = []
            for idx, (checkbox_text, initial_value) in enumerate(self._checkbox_items):
                checkbox_var = IntVar(value=initial_value)
                checkbox = CTkCheckBox(
                    master=self,
                    text=checkbox_text,
                    variable=checkbox_var,
                    fg_color="transparent",  # Modify this according to your theme
                    font=self._font,
                )
                checkbox.grid(row=idx + 3, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="w")
                self.checkboxes.append((checkbox_var, checkbox_text))

        # ... (existing code remains the same)

    def _ok_event(self, event=None):
        self._user_input = self._entry.get()
        # Include checkbox values in the result
        checkbox_results = [(text, var.get()) for var, text in self.checkboxes]
        self._user_input += checkbox_results
        self.grab_release()
        self.destroy()

    # ... (existing code remains the same)

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input
