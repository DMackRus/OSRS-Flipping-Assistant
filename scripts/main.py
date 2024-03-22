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

dark_gray = "#333333"
vibrant_yellow = "#FFD700"

def main():

    root = Tk()

    RS_itemsManager = ItemsManager()

    gui = RuneScapeGUI(root, RS_itemsManager)

    mainloop()

    # itemids = RS_itemsManager.itemIds

    # update flipping items json, with item ids

    # for i in range(len(RS_itemsManager.flippingItemNames)):
    #     historical_data = RS_itemsManager.get_historical_data(RS_itemsManager.lookupItemId(RS_itemsManager.flippingItemNames[i]))
    #     RS_itemsManager.save_price_data(historical_data, RS_itemsManager.flippingItemNames[i])

    # When program starts up.






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

    # print("--------------------------------------- printed flipping item names -----------------------------")
    # runeScapeGUI = GUI.runeScapeGUI(root, RS_itemsManager)

    # TransposedItems = itemIds.T

    # print(TransposedItems.head(5))

    # sortedItems = TransposedItems.sort_values(by=['name'], ascending=1)

    # print(sortedItems.head(5))

    # mainloop()

if __name__ == "__main__":
    main()