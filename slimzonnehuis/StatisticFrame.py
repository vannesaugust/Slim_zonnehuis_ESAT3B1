from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from time import strftime
from FrameEnergieprijs import FrameEnergieprijs
from FramePvsC import FramePvsC
from FrameTotalen import FrameTotalen
from FrameVerbruikers import FrameVerbruikers
from FrameWeer import FrameWeer

class StatisticFrame(CTkFrame):
    def __init__(self, parent):
        CTkFrame.__init__(self,parent, width=3840, height=2160)
        self.pack_propagate('false')

        self.grid_columnconfigure((0, 1), uniform="uniform", weight=2)
        self.grid_columnconfigure(2, uniform="uniform", weight=3)
        self.grid_rowconfigure(0, uniform="uniform", weight=2)
        self.grid_rowconfigure(1, uniform="uniform", weight=1)

        frame_PvsC = FramePvsC(self)
        frame_verbruikers = FrameVerbruikers(self)
        frame_energieprijs = FrameEnergieprijs(self)
        frame_weer = FrameWeer(self)
        frame_totalen = FrameTotalen(self)

        frame_PvsC.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        frame_verbruikers.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        frame_energieprijs.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        frame_weer.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        frame_totalen.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')