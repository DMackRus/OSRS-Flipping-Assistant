from tkinter import *
import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from ttkwidgets.autocomplete import AutocompleteEntry

class runeScapeGUI():
    def __init__(self, master, flippingitemNames):
        self.master = master
        self.master.title("GUI")
        self.master.geometry("500x500")
        self.master.resizable(False, False)

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.master.title('Runescape Stock Market')

        self.data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        # the figure that will contain the plot
        fig = plt.Figure(figsize = (9, 5),
                    dpi = 100)
    
        # adding the subplot
        plot1 = fig.add_subplot(111)
    
        # plotting the graph
        plot1.plot(self.data)
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                master = self.master)  
        canvas.draw()
  
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                    self.master)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

        frame = Frame(self.master, bg='#f25252')
        
        entry = AutocompleteEntry(
        frame, 
        width=30, 
        font=('Times', 18),
        completevalues=flippingitemNames,
        )
        entry.bind('<FocusOut>', self.callback)
        entry.pack()

        frame.pack(expand=True)

    def callback(self, event):
        print("clicked!")
