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
import os
import utils
from pathlib import Path

class multipliers(Enum):
    THOUSAND = 1
    MILLION = 2
    BILLION = 3

class RuneScapeGUI():
    def __init__(self, master, ItemsManager):
        self.master = master
        self.master.title("GUI")
        self.master.geometry("1400x700")
        self.master.resizable(True, True)
        self.items_manager = ItemsManager

        # self.frame = tk.Frame(self.master)
        # self.frame.pack()
        self.displayMode = 0
        self.displayedItemName = None

        self.master.title('Runescape Stock Market')

        self.totalGraphData = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        self.setup_frames()

        # self.updatePlot(self.displayedItemName, self.displayMode)
  
        # # placing the canvas on the Tkinter window
        # self.canvas.get_tk_widget().pack()
    
        # # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(self.canvas,
        #                             self.master)
        # toolbar.update()
    
        # # placing the toolbar on the Tkinter window
        # self.canvas.get_tk_widget().pack()

        # frame = Frame(self.master, bg='#f25252')
        # frame.pack(expand=True)

        # self.entry = AutocompleteEntry(
        # frame, 
        # width=30, 
        # font=('Times', 18),
        # completevalues=self.items_manager.flippingItemNames,
        # )
        # self.entry.bind('<FocusOut>', self.searchBar_callback)
        # self.entry.pack()

        # frame.pack(expand=True)

        # modes = ('All', '6 Months', '3 Months', 'Month', 'Week')
        # var = tk.Variable(value=modes)
        # listbox = tk.Listbox(
        #     self.master, 
        #     listvariable=var, 
        #     height=6,
        #     selectmode=tk.SINGLE,
        # )
        # listbox.pack(expand=True, fill=tk.BOTH)
        # listbox.bind('<<ListboxSelect>>', self.displayMode_callback)
    def setup_frames(self):
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.grid(row=0, column=0, columnspan=2)

        self.plot_left_frame = tk.Frame(self.master, bg='red')
        self.plot_left_frame.grid(row=1, column=0)

        self.plot_right_frame = tk.Frame(self.master, bg='blue')
        self.plot_right_frame.grid(row=1, column=1)

        self.general_controls_frame = tk.Frame(self.master, bg="black")
        self.general_controls_frame.grid(row=2, column=0, columnspan=2)

        self.add_plots(self.plot_frame)
        self.add_controls()

    def add_plots(self, frame):
        # Figures to show item price data
        self.figure_left = plt.Figure(figsize = (5, 3),
                    dpi = 100)
        
        self.figure_right = plt.Figure(figsize = (5, 3),
                    dpi = 100)
    
        # adding the plot to the figure
        self.plot_left = self.figure_left.add_subplot(111)
        self.plot_right = self.figure_right.add_subplot(111)   

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas_left = FigureCanvasTkAgg(self.figure_left,
                                master = frame)  
        
        self.canvas_right = FigureCanvasTkAgg(self.figure_right,
                                master = frame)
        
        self.canvas_left_widget = self.canvas_left.get_tk_widget()
        self.canvas_right_widget = self.canvas_right.get_tk_widget()

        self.canvas_left_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_right_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def add_controls(self):

        button_texts = ["all", "6 months", "3 months", "1 month", "week"]

        self.item_select_left = AutocompleteEntry(
            self.plot_left_frame, 
            width=30, 
            font=('Times', 18),
            completevalues=self.items_manager.custom_items.keys(),
        )
        self.item_select_left.bind('<FocusOut>', self.searchbar_callback_left)
        self.item_select_left.pack()

        # frame.pack(expand=True)
        for text in button_texts:
            button = tk.Button(self.plot_left_frame, text=text, command=lambda period=text, plot="left": self.history_button_click(period, plot))
            button.pack(side=tk.RIGHT, anchor=tk.NE, padx=5, pady=5)

        self.item_select_right = AutocompleteEntry(
            self.plot_right_frame, 
            width=30, 
            font=('Times', 18),
            completevalues=self.items_manager.custom_items.keys(),
        )
        self.item_select_right.bind('<FocusOut>', self.searchbar_callback_right)
        self.item_select_right.pack()

        for text in button_texts:
            button = tk.Button(self.plot_right_frame, text=text, command=lambda period=text, plot = "right": self.history_button_click(period, plot))
            button.pack(side=tk.RIGHT, anchor=tk.NE, padx=5, pady=5)

        button = tk.Button(self.general_controls_frame, text="Search", command=self.test_button_click)
        button.pack(side=tk.TOP, padx=5, pady=5)

    # ----------------- Callbacks -----------------
    def test_button_click(self):
        print("test button click")
        

    def history_button_click(self, period, plot):
        print(f"period: {period}, plot: {plot}")
        self.displayMode = self.get_display_mode(period)

    def displayMode_callback(self, event):
        self.displayMode = event.widget.curselection()[0]
        self.updatePlot(self.displayedItemName, self.displayMode)

    # Would be nice to combine these two functions into one function using lambda, but i cant 
    # figure it out
    def searchbar_callback_left(self, event):
        item_name = self.item_select_left.get()

        if item_name not in self.items_manager.custom_items.keys():
            print("Item not found")
            return
            
        
        self.update_plot(item_name, self.displayMode)

    def searchbar_callback_right(self, event):
        item_name = self.item_select_right.get()

        if item_name not in self.items_manager.custom_items.keys():
            print("Item not found")
            return
        
        self.update_plot(item_name, self.displayMode)

    def update_plot(self, item_name, display_mode=0):

        graph_data = None
        file = "data/" + str(item_name) + "/price_history.pkl"

        # Check if item price historry file exists
        if os.path.exists(file):
            print("data file doesnt exist, lets create it")
            graph_data = utils.load_data(file)
        else:
            graph_data = self.items_manager.get_historical_data(item_name)
        
        prices, time_labels = self.reduce_display_data(graph_data, display_mode)
        self.draw_graph(prices)

    def reduce_display_data(self, graph_data, mode):

        time_labels = graph_data['time_stamps']
        prices = graph_data['values']

        if(mode == 0):
            return prices, time_labels
        elif(mode == 1):
            return prices[-180:], time_labels[-180:]
        elif(mode == 2):
            return prices[-90:], time_labels[-99:]
        elif(mode == 3):
            return prices[-30:], time_labels[-30:]
        elif(mode == 4):
            return prices[-7:], time_labels[-7:]


    def draw_graph(self, graph_data):
        print("draw graph")
        print(graph_data)

        if(graph_data[0] > 1_000_000_000):
            graph_data = [x / 1_000_000_000 for x in graph_data]
            suffix = "b"
        elif(graph_data[0] > 1_000_000):
            graph_data = [x / 1_000_000 for x in graph_data]
            suffix = "m"
        elif(graph_data[0] > 1_000):
            graph_data = [x / 1_000 for x in graph_data]
            suffix = "k"

        plot_data = graph_data

        self.plot_left.cla()
        self.plot_left.plot(plot_data)

        y_ticks = self.plot_left.get_yticks()
        new_y_ticks = []
        for i in range(len(y_ticks)):
            y_ticks[i] = y_ticks[i]
            new_y_ticks.append(f'{y_ticks[i]:g}' + suffix)

        self.plot_left.set_yticklabels(new_y_ticks)

        self.canvas_left.draw()

    def load_price_data_csv(self, itemName):
        filePath = "pastPrices/" + itemName + ".csv"
        print(filePath)

        my_data = genfromtxt(filePath, delimiter=',')

        return my_data
