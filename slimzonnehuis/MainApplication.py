from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from time import strftime
from HomeFrame import HomeFrame
from ControlFrame import ControlFrame
from StatisticFrame import StatisticFrame

set_appearance_mode("system")
set_default_color_theme("blue")

class MainApplication(CTk):
    def __init__(self):
        super().__init__()

        self.geometry('3840x2160')
        self.title("SMART SOLAR HOUSE")
        self.iconbitmap('solarhouseicon.ico')

        my_notebook = ttk.Notebook(self)
        my_notebook.pack()

        frame_home = HomeFrame(my_notebook)
        frame_controls = ControlFrame(my_notebook)
        frame_statistics = StatisticFrame(my_notebook)

        frame_home.pack(fill='both', expand=1)
        frame_controls.pack(fill='both', expand=1)
        frame_statistics.pack(fill='both', expand=1)

        my_notebook.add(frame_home, text='HOME')
        my_notebook.add(frame_controls, text='CONTROLS')
        my_notebook.add(frame_statistics, text='STATISTICS')


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()