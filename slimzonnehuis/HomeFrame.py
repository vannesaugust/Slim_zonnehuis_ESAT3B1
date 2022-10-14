from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from time import strftime

class HomeFrame(CTkFrame):
    def __init__(self, parent):
        CTkFrame.__init__(self,parent, width=3840, height=2160)
        self.pack_propagate('false')

        home_title = CTkLabel(self, text='SMART SOLAR HOUSE')
        home_subtitle = CTkLabel(self, text='Door August Vannes, Jonas Thewis, Lander Verhoeven, Ruben Vanherpe,'
                                                  'Tibo Mattheus en Tijs Motmans')

        home_title.pack()
        home_subtitle.pack()


