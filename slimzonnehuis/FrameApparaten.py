from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from time import strftime
from NewDevice import NewDevice

class FrameApparaten(CTkFrame):
    def __init__(self, parent):
        CTkFrame.__init__(self,parent, bd=5, corner_radius=10)
        self.pack_propagate('false')

        self.grid_rowconfigure((0,2), uniform="uniform", weight=1)
        self.grid_rowconfigure(1, uniform="uniform", weight=16)
        self.grid_columnconfigure(0, uniform="uniform", weight=1)

        btn_newdevice = CTkButton(self, text='Add new device', command=self.new_device)
        btn_newdevice.grid(row=2, padx=10, pady=5, sticky='nsew')
        title = CTkLabel(self, text="CURRENT DEVICES")
        title.grid(row=0, sticky = 'nsew')
        frame1 = CTkFrame(self)
        frame1.grid(row=1, padx=10, pady=5, sticky='nsew')

        my_canvas = CTkCanvas(frame1)
        my_canvas.pack(side='left',fill='both', expand=1)

        my_scrollbar = CTkScrollbar(frame1,orientation='vertical', command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT,fill='y')

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        frame2 = CTkFrame(my_canvas, corner_radius=0)
        frame2.pack(fill='both',expand=1)

        lijst_apparaten = []

        #frigo = APPARAAT(frame2, 'frigo')
        #wasmachine = APPARAAT(frame2, 'wasmachine')

    def new_device(self):
        window_new_device = NewDevice()

"""
class APPARAAT(CTkFrame): 
    def __init__(self, parent, naam_apparaat,lijst_apparaten):
        lijst_apparaten.add
        CTkFrame.__init__(self, parent,bd=5, corner_radius=5)
        self.pack_propagate('false')
        self.grid()
        
        
        title = CTkLabel(self, text=naam_apparaat)
        CTkLabel.grid(row=0, column=0)
"""




