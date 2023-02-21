import json 
import requests
from itemClass import item
import numpy as np
import pandas as pd
import os

class itemsManager():
    def __init__(self):
        self.itemIds = json.load(open('items-search.json'))
        tempFlipOpen = json.load(open('flippingItems.json'))
        self.flippingItemNames = []
        for i in range(len(tempFlipOpen)):
            self.flippingItemNames.append(tempFlipOpen[i]["name"])

        self.items = []

        for i in range(len(self.flippingItemNames)):
            itemId = self.lookupItemId(self.flippingItemNames[i])

            if(os.path.exists('items/' + self.flippingItemNames[i] + '/trackData.json')):
                with open('items/' + self.flippingItemNames[i] + '/trackData.json', 'r') as outfile:
                    json_data = json.load(outfile)

                self.items.append(item(self.flippingItemNames[i], itemId, json_data["high price alert"], json_data["low price alert"], json_data["last update date"]))
            else:
                self.createJsonFile(self.flippingItemNames[i])

                self.items.append(item(self.flippingItemNames[i], itemId, 0, 0, 0))

    def createJsonFile(self, itemName):
        baseDir = "items/"

        os.makedirs(baseDir + itemName, exist_ok=True)

        temp = '{ "low price alert":0, "high price alert":0, "last update date":"0"}'

        with open('items/' + itemName + '/trackData.json', 'w') as outfile:
            outfile.write(temp)

    def getCurrentPriceOfItem(self):

        base_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"

        end_url = str(self.id) + ".json"

        request_url = base_url + end_url

        api_return = requests.get(request_url).json()

        #print(api_return["average"])
        #print(list(api_return["average"])[-1])
        stringPrice = str(api_return["average"][list(api_return["average"])[-1]])

        itemPrice = float(stringPrice)

        return itemPrice

    def getHistoricalData(self, itemId):

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

    def saveHistoricalPriceToCSV(self, priceHistory, itemName):
        priceHistory.tofile('pastPrices/' + itemName + '.csv', sep = ',')

    def lookupItemId(self, itemName):
        itemId = 0
        for i in range(len(self.itemIds)):
            try:
                if(self.itemIds[str(i)]["name"] == itemName):
                    itemId = int(self.itemIds[str(i)]["id"])
                    break
            except:
                pass

        return itemId

