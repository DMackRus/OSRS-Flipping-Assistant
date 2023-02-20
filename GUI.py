from tkinter import *
import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from numpy import genfromtxt
from ttkwidgets.autocomplete import AutocompleteEntry
from enum import Enum
import json
from itemsManagerClass import itemsManager

class multipliers(Enum):
    THOUSAND = 1
    MILLION = 2
    BILLION = 3

class runeScapeGUI():
    def __init__(self, master, itemsManager):
        self.master = master
        self.master.title("GUI")
        self.master.geometry("700x700")
        self.master.resizable(True, True)
        self.itemsManager = itemsManager

        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.displayMode = 0
        self.displayedItemName = "Twisted bow"

        self.master.title('Runescape Stock Market')

        self.totalGraphData = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        priceSuffixes = ["k", "m", "b"]

        # the figure that will contain the plot
        self.fig = plt.Figure(figsize = (9, 5),
                    dpi = 100)
    
        # adding the subplot
        self.plot1 = self.fig.add_subplot(111)
    
        # plotting the graph
        

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig,
                                master = self.master)  

        self.updatePlot(self.displayedItemName, self.displayMode)
  
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
        completevalues=self.itemsManager.flippingItemNames,
        )
        self.entry.bind('<FocusOut>', self.searchBar_callback)
        self.entry.pack()

        frame.pack(expand=True)

        modes = ('All', '6 Months', '3 Months', 'Month', 'Week')
        var = tk.Variable(value=modes)
        listbox = tk.Listbox(
            self.master, 
            listvariable=var, 
            height=6,
            selectmode=tk.SINGLE,
        )
        listbox.pack(expand=True, fill=tk.BOTH)
        listbox.bind('<<ListboxSelect>>', self.displayMode_callback)

    def displayMode_callback(self, event):
        self.displayMode = event.widget.curselection()[0]
        self.updatePlot(self.displayedItemName, self.displayMode)

    def searchBar_callback(self, event):
        self.displayedItemName = self.entry.get()

        self.updatePlot(self.displayedItemName, self.displayMode)

    def updatePlot(self, itemName, displayMode=0):
        graphData = self.loadHistoricData(itemName)
        graphData = self.reduceDisplayData(graphData, displayMode)
        self.drawGraph(graphData)


    # mode 0 = all data
    # mode 1 = last week
    # mode 2 = last 1 month
    # mode 3 = 1 month
    # mode 4 = 3 months
    def reduceDisplayData(self, graphData, mode):
        if(mode == 0):
            return graphData
        elif(mode == 1):
            return graphData[-180:]
        elif(mode == 2):
            return graphData[-90:]
        elif(mode == 3):
            return graphData[-30:]
        elif(mode == 4):
            return graphData[-7:]


    def drawGraph(self, graphData):

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
            y_ticks[i] = y_ticks[i]
            new_y_ticks.append(f'{y_ticks[i]:g}' + suffix)

        self.plot1.set_yticklabels(new_y_ticks)

        self.canvas.draw()

    def loadHistoricData(self, itemName):
        filePath = "pastPrices/" + itemName + ".csv"
        print(filePath)

        my_data = genfromtxt(filePath, delimiter=',')

        return my_data
