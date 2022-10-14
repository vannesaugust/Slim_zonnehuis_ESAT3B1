from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from time import strftime
from FrameApparaten import FrameApparaten
from FrameBatterijen import FrameBatterijen
from FrameTemperatuur import FrameTemperatuur
from FrameTime import FrameTime

class ControlFrame(CTkFrame):
    def __init__(self, parent):
        CTkFrame.__init__(self,parent, width=3840, height=2160)
        self.pack_propagate('false')

        self.grid_columnconfigure((0, 1), uniform="uniform", weight=1)
        self.grid_rowconfigure(0, uniform="uniform", weight=1)
        self.grid_rowconfigure(1, uniform="uniform", weight=3)
        self.grid_rowconfigure(2, uniform="uniform", weight=2)

        frame_time = FrameTime(self)
        frame_temperatuur = FrameTemperatuur(self)
        frame_batterijen = FrameBatterijen(self)
        frame_apparaten = FrameApparaten(self)

        frame_time.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        frame_temperatuur.grid(row=1, column=0, padx=5, sticky='nsew')
        frame_batterijen.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        frame_apparaten.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky='nsew')