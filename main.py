import numpy as np
import json
import time
from tkinter import *
from collections import OrderedDict
import pandas as pd
from ttkwidgets.autocomplete import AutocompleteEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#import customtkinter as ctk
from itemsManagerClass import itemsManager
import GUI

def main():
                
    root = Tk()
    RS_itemsManager = itemsManager()
    print("made items manager")
    print(RS_itemsManager.flippingItemNames)
    print("--------------------------------------- printed flipping item names -----------------------------")
    runeScapeGUI = GUI.runeScapeGUI(root, RS_itemsManager)

    # TransposedItems = itemIds.T

    # print(TransposedItems.head(5))

    # sortedItems = TransposedItems.sort_values(by=['name'], ascending=1)

    # print(sortedItems.head(5))

    mainloop()

def updatePrices():
    todayPrices = np.zeros(2)


if __name__ == "__main__":
    main()