import numpy as np
import json
import time
from tkinter import *
from collections import OrderedDict
from ttkwidgets.autocomplete import AutocompleteEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#import customtkinter as ctk
from items_manager import ItemsManager, Item
from GUI import RuneScapeGUI
import os

def main():

    root = Tk()

    RS_itemsManager = ItemsManager()

    gui = RuneScapeGUI(root, RS_itemsManager)

    mainloop()

if __name__ == "__main__":
    main()