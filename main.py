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
import os

def main():
    baseDir = "items/"
                
    root = Tk()
    RS_itemsManager = itemsManager()
    print("made items manager")
    print(RS_itemsManager.flippingItemNames)

    # test = {"low price alert":"0","high price alert":"0","last update date":"0"}
    # test = '{ "low price alert":10, "high price alert":0, "last update date":"0"}'
    # testjson = json.loads(test)
    # print(testjson["low price alert"])

    # with open('items/Abyssal whip/json_data.json', 'w') as outfile:
    #     outfile.write(test)

    # with open('json_data.json', 'w') as outfile:
    #     json.dump(test, outfile)
    #print(testjson[0])
    # for i in range(len(RS_itemsManager.flippingItemNames)):
    #     os.makedirs(baseDir + RS_itemsManager.flippingItemNames[i], exist_ok=True)

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