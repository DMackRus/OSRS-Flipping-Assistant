from tkinter import *
import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from numpy import genfromtxt
from ttkwidgets.autocomplete import AutocompleteEntry
from enum import Enum

class multipliers(Enum):
    THOUSAND = 1
    MILLION = 2
    BILLION = 3

class runeScapeGUI():
    def __init__(self, master, flippingitemNames):
        self.master = master
        self.master.title("GUI")
        self.master.geometry("700x700")
        self.master.resizable(True, True)

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.master.title('Runescape Stock Market')

        self.totalGraphData = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        priceSuffixes = ["k", "m", "b"]

        # the figure that will contain the plot
        self.fig = plt.Figure(figsize = (9, 5),
                    dpi = 100)
    
        # adding the subplot
        self.plot1 = self.fig.add_subplot(111)
    
        # plotting the graph
        self.plot1.plot(self.totalGraphData)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig,
                                master = self.master)  
        self.canvas.draw()
  
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas,
                                    self.master)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()

        frame = Frame(self.master, bg='#f25252')
        frame.pack(expand=True)

        self.entry = AutocompleteEntry(
        frame, 
        width=30, 
        font=('Times', 18),
        completevalues=flippingitemNames,
        )
        self.entry.bind('<FocusOut>', self.callback)
        self.entry.pack()

        frame.pack(expand=True)

    def callback(self, event):
        itemName = self.entry.get()
        self.totalGraphData = self.loadHistoricData(itemName)

        self.drawGraph(self.totalGraphData, 0)


    def drawGraph(self, graphData, mode):

        if(graphData[0] > 1_000_000_000):
            graphData = graphData / 1_000_000_000
            suffix = "b"
        elif(graphData[0] > 1_000_000):
            graphData = graphData / 1_000_000
            suffix = "m"
        elif(graphData[0] > 1_000):
            graphData = graphData / 1_000
            suffix = "k"

        plotData = graphData

        self.plot1.cla()
        self.plot1.plot(plotData)

        y_ticks = self.plot1.get_yticks()
        new_y_ticks = []
        for i in range(len(y_ticks)):
            new_y_ticks.append(str(y_ticks[i]) + suffix)

        self.plot1.set_yticklabels(new_y_ticks)

        self.canvas.draw()

    def loadHistoricData(self, itemName):
        filePath = "pastPrices/" + itemName + ".csv"
        print(filePath)

        my_data = genfromtxt(filePath, delimiter=',')

        return my_data
