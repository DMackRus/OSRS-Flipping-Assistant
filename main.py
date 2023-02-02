import requests
import numpy as np
import json
import time
from tkinter import *
from collections import OrderedDict
import pandas as pd
from ttkwidgets.autocomplete import AutocompleteEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import customtkinter as ctk
import itemClass 
import GUI

loadHistoricalData = False
itemIds = json.load(open('items-search.json'))

#itemIds = pd.read_json('items-search.json')
flippingItemNames = json.load(open('flippingItems.json'))

def main():

    flippingitemNames = []
    items = []

    

    if(True):
        for i in range(len(flippingItemNames)):
            print(flippingItemNames[i]["name"])
            itemId = lookupItemId(flippingItemNames[i]["name"])
            print("item id: " + str(itemId))

            items.append(itemClass.item(flippingItemNames[i]["name"], itemId, 0))

            flippingitemNames.append(flippingItemNames[i]["name"])

            if(loadHistoricalData):
                historicalData = getHistoricalData(itemId)
                saveHistoricalPriceToCSV(historicalData, flippingItemNames[i]["name"])
                # itemPrice = getCurrentPriceOfItem(itemId)

                # print("price of " +  flippingItemNames[i]["name"] + ": " + str(itemPrice))

                
    root = Tk()
    runeScapeGUI = GUI.runeScapeGUI(root, flippingitemNames)

    print(items[0].__str__())

    # TransposedItems = itemIds.T

    # print(TransposedItems.head(5))

    # sortedItems = TransposedItems.sort_values(by=['name'], ascending=1)

    # print(sortedItems.head(5))

    mainloop()

def updatePrices():

    todayPrices = np.zeros(2)


def getCurrentPriceOfItem(itemId):

    base_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"

    end_url = str(itemId) + ".json"

    request_url = base_url + end_url

    api_return = requests.get(request_url).json()

    #print(api_return["average"])
    #print(list(api_return["average"])[-1])
    stringPrice = str(api_return["average"][list(api_return["average"])[-1]])

    itemPrice = float(stringPrice)

    return itemPrice

def getHistoricalData(itemId):

    base_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"

    end_url = str(itemId) + ".json"

    request_url = base_url + end_url

    api_return = requests.get(request_url).json()

    historyPrices = np.zeros(len(api_return["average"]))

    for i in range(len(api_return["average"])):
        stringPrice = str(api_return["average"][list(api_return["average"])[i]])

        itemPrice = float(stringPrice)

        historyPrices[i] = itemPrice

    return historyPrices


def saveHistoricalPriceToCSV(priceHistory, itemName):

    priceHistory.tofile('pastPrices/' + itemName + '.csv', sep = ',')

def lookupItemId(itemName):
    itemId = 0

    for i in range(len(itemIds)):

        try:
            if(itemIds[str(i)]["name"] == itemName):
                print(itemIds[str(i)]["id"])
                itemId = int(itemIds[str(i)]["id"])
                break
        except:
            pass

    return itemId

if __name__ == "__main__":
    main()