from tkinter import *
import tkinter as tk
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
from dataclasses import dataclass, field
from items_manager import ItemsManager
from mailer import Mailer

dark_gray = "#333333"
lighter_gray = "#444444"
white = "#FFFFFF"
vibrant_yellow = "#FFD700"
dark_blue = "#00008B"

@dataclass
class PlotData():
    item_name: str = "None"
    data: list = field(default_factory=list)
    display_mode: str = "all"
    high_alert: float = None
    low_alert: float = None
    

class RuneScapeGUI():
    def __init__(self, master, ItemsManager):
        self.master = master
        self.master.title("GUI")
        self.master.geometry("1000x500")
        self.master.resizable(True, True)
        self.items_manager = ItemsManager

        self.display_mode = "all"
        self.displayedItemName = None

        self.master.title('OSRS Flipping assistant')
        self.mailer = Mailer()
        
        # Set color of self.master
        self.master.configure(bg=dark_gray)

        self.setup_frames()

        # Instantiate two plots as default on program load
        self.plots_data = [PlotData("Toxic blowpipe (empty)"), PlotData("Granite maul")]

        self.update_plot("Toxic blowpipe (empty)", 0, "all")
        self.update_plot("Granite maul", 1, "all")

        self.mailer.send_email("OSRS Flipping assistant started", "Hey, just to let you know, the program has started :).")

    def setup_frames(self):
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.grid(row=0, column=0, columnspan=2)

        self.plot_left_frame = tk.Frame(self.master, bg=dark_gray)
        self.plot_left_frame.grid(row=1, column=0)

        self.plot_right_frame = tk.Frame(self.master, bg=dark_gray)
        self.plot_right_frame.grid(row=1, column=1)

        self.general_controls_frame = tk.Frame(self.master, bg=dark_gray)
        self.general_controls_frame.grid(row=2, column=0, columnspan=2)

        self.add_plots(self.plot_frame)
        self.add_controls()

    def add_plots(self, frame):
        # Figures to show item price data
        self.figure_left = plt.Figure(figsize = (5, 3),
                    dpi = 100)
        
        self.figure_right = plt.Figure(figsize = (5, 3),
                    dpi = 100)
        
        # Select colors for figure
        self.figure_left.set_facecolor(dark_gray)
        self.figure_right.set_facecolor(dark_gray)
    
        # adding the plot to the figure
        self.plot_left = self.figure_left.add_subplot(111)
        self.plot_right = self.figure_right.add_subplot(111)   

        # Select colors for plots
        self.plot_left.set_facecolor(lighter_gray)
        self.plot_right.set_facecolor(lighter_gray)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas_left = FigureCanvasTkAgg(self.figure_left,
                                master = frame)  
        
        self.canvas_right = FigureCanvasTkAgg(self.figure_right,
                                master = frame)
        
        self.canvas_left.mpl_connect('motion_notify_event', lambda event, plot="left": self.on_hover(event, plot))
        self.canvas_right.mpl_connect('motion_notify_event', lambda event, plot="right": self.on_hover(event, plot))
        
        self.canvas_left_widget = self.canvas_left.get_tk_widget()
        self.canvas_right_widget = self.canvas_right.get_tk_widget()

        self.canvas_left_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_right_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def add_controls(self):

        button_texts = ["all", "6 months", "3 months", "1 month", "week"]

        # ----------------- left control panel -----------------------------
        self.item_select_left = AutocompleteEntry(
            self.plot_left_frame, 
            width=30, 
            font=('Times', 18),
            completevalues=self.items_manager.custom_items.keys(),
        )
        self.item_select_left.bind('<FocusOut>', self.searchbar_callback_left)
        self.item_select_left.pack()

        for text in button_texts:
            button = tk.Button(self.plot_left_frame, text=text, command=lambda period=text, plot="left": self.history_button_click(period, plot))
            button.pack(side=tk.RIGHT, anchor=tk.NE, padx=5, pady=5)

        button = tk.Button(self.plot_left_frame, text="Save alerts", command= lambda plot="left": self.save_alerts(plot))
        button.pack(side=tk.TOP, anchor=tk.NE, padx=5, pady=5)

        # ----------------- right control panel -----------------------------

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

        button = tk.Button(self.plot_right_frame, text="Save alerts", command= lambda plot="right": self.save_alerts(plot))
        button.pack(side=tk.TOP, anchor=tk.NE, padx=5, pady=5)

        # ----------------- general controls -----------------------------

        button = tk.Button(self.general_controls_frame, text="Search", command=self.test_button_click)
        button.pack(side=tk.TOP, padx=5, pady=5)

    # ----------------- Callbacks -----------------
    def test_button_click(self):
        print("test button click")
        utils.capture_window(self.master)
        

    def history_button_click(self, period, plot):
        print(f"period: {period}, plot: {plot}")

        self.display_mode = period
        if(plot == "left"):
            plot_data = self.plots_data[0]
            item_name = plot_data.item_name
            self.update_plot(item_name, 0, period)
        elif(plot == "right"):
            plot_data = self.plots_data[1]
            item_name = plot_data.item_name
            self.update_plot(item_name, 1, period)

    def save_alerts(self, plot):

        if(plot == "left"):
            plot_data = self.plots_data[0]
            
        elif(plot == "right"):
            plot_data = self.plots_data[1]

        item_name = plot_data.item_name

        file = "data/" + str(item_name) + "/alerts.pkl"
        alerts = {"high_alert": plot_data.high_alert, "low_alert": plot_data.low_alert}
        utils.save_data(alerts, file)


    # Would be nice to combine these two functions into one function using lambda, but i cant 
    # figure it out
    def searchbar_callback_left(self, event):
        item_name = self.item_select_left.get()

        if item_name not in self.items_manager.custom_items.keys():
            print("Item not found")
            return
            
        self.update_plot(item_name, 0, self.display_mode)

    def searchbar_callback_right(self, event):
        item_name = self.item_select_right.get()

        if item_name not in self.items_manager.custom_items.keys():
            print("Item not found")
            return
        
        self.update_plot(item_name, 1, self.display_mode)

    def on_hover(self, event, plot):

        # If the left mouse button is clicked
        if event.button == 1:
            if event.xdata is not None and event.ydata is not None:

                if(plot == "left"):
                    plot_data = self.plots_data[0]
                    plot_data.high_alert = event.ydata
                    plot = self.plot_left
                    canvas = self.canvas_left

                elif(plot == "right"):
                    plot_data = self.plots_data[1]
                    plot_data.high_alert = event.ydata
                    plot = self.plot_right
                    canvas = self.canvas_right

                self.draw_graph(plot_data, plot, canvas)

        # if right mouse button is clicked
        elif event.button == 3:
            if event.xdata is not None and event.ydata is not None:

                if(plot == "left"):
                    plot_data = self.plots_data[0]
                    plot_data.low_alert = event.ydata
                    plot = self.plot_left
                    canvas = self.canvas_left

                elif(plot == "right"):
                    plot_data = self.plots_data[1]
                    plot_data.low_alert = event.ydata
                    plot = self.plot_right
                    canvas = self.canvas_right

                self.draw_graph(plot_data, plot, canvas)

    def update_plot(self, item_name, plot_number, display_mode="all"):

        graph_data = None
        file = "data/" + str(item_name) + "/price_history.pkl"

        # Check if item price history file exists
        if os.path.exists(file):
            graph_data = utils.load_data(file)
        else:
            graph_data = self.items_manager.get_historical_data(item_name)

        # Check if item price alerts exist
        alerts_file = "data/" + str(item_name) + "/alerts.pkl"
        if os.path.exists(alerts_file):
            alerts = utils.load_data(alerts_file)
            if "high_alert" in alerts:
                self.plots_data[plot_number].high_alert = alerts["high_alert"]
            if "low_alert" in alerts:
                self.plots_data[plot_number].low_alert = alerts["low_alert"]

        # TODO this could be improved, maybe one day we will have more than 2 plots
        if(plot_number == 0):
            plot = self.plot_left
            canvas = self.canvas_left
            plot_data = self.plots_data[0]
        else:
            plot = self.plot_right
            canvas = self.canvas_right
            plot_data = self.plots_data[1]
        
        prices, time_labels = self.reduce_display_data(graph_data, display_mode)

        plot_data.data = prices
        plot_data.item_name = item_name
        plot_data.display_mode = display_mode

        self.draw_graph(plot_data, plot, canvas)

    def reduce_display_data(self, graph_data, mode):

        time_labels = graph_data['time_stamps']
        prices = graph_data['values']

        if(mode == "all"):
            return prices, time_labels
        elif(mode == "6 months"):
            return prices[-180:], time_labels[-180:]
        elif(mode == "3 months"):
            return prices[-90:], time_labels[-90:]
        elif(mode == "1 month"):
            return prices[-30:], time_labels[-30:]
        elif(mode == "week"):
            return prices[-7:], time_labels[-7:]

    def draw_graph(self, plot_data, plot, canvas):

        graph_data = plot_data.data
        item_name = plot_data.item_name
        high_horiozntal = plot_data.high_alert
        low_horizontal = plot_data.low_alert

        if(graph_data[0] > 1_000_000_000):
            graph_data = [x / 1_000_000_000 for x in graph_data]
            suffix = "b"
        elif(graph_data[0] > 1_000_000):
            graph_data = [x / 1_000_000 for x in graph_data]
            suffix = "m"
        elif(graph_data[0] > 1_000):
            graph_data = [x / 1_000 for x in graph_data]
            suffix = "k"

        plot.cla()
        plot.plot(graph_data)

        plot.set_title(item_name)
        plot.set_xlabel("Time")
        plot.set_ylabel("Price")

        y_ticks = plot.get_yticks()
        new_y_ticks = []
        for i in range(len(y_ticks)):
            y_ticks[i] = y_ticks[i]
            new_y_ticks.append(f'{y_ticks[i]:g}' + suffix)

        plot.set_yticklabels(new_y_ticks)

        if(high_horiozntal is not None):
            plot.ax_hline = plot.axhline(y=high_horiozntal, color=vibrant_yellow, linestyle='--')

        if(low_horizontal is not None):
            plot.ax_hline = plot.axhline(y=low_horizontal, color=vibrant_yellow, linestyle='--')

        canvas.draw()
    

def main():

    root = Tk()

    RS_itemsManager = ItemsManager()

    gui = RuneScapeGUI(root, RS_itemsManager)

    mainloop()

if __name__ == "__main__":
    main()
