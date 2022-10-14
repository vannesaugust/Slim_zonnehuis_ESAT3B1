from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from tkinter import ttk

class NewDevice(CTkToplevel):
    def __init__(self):
        CTkToplevel.__init__(self)

        self.iconbitmap('solarhouseicon.ico')
        self.title('Add a new device')
        self.geometry('700x700')