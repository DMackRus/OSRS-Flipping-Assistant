import json 
import requests
from itemClass import item
import numpy as np
import pandas as pd
import os
import utils

class ItemsManager():

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

    def create_json_file(self, itemName):
        baseDir = "items/"

        os.makedirs(baseDir + itemName, exist_ok=True)

        temp = '{ "low price alert":0, "high price alert":0, "last update date":"0"}'

        with open('items/' + itemName + '/trackData.json', 'w') as outfile:
            outfile.write(temp)

    def get_current_price_of_item(self):

        base_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"

        end_url = str(self.id) + ".json"

        request_url = base_url + end_url

        api_return = requests.get(request_url).json()

        stringPrice = str(api_return["average"][list(api_return["average"])[-1]])

        itemPrice = float(stringPrice)

        return itemPrice

    def get_historical_data(self, itemId):

        base_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"

        end_url = str(itemId) + ".json"

        request_url = base_url + end_url

        api_return = requests.get(request_url).json()

        history_prices = {
            "time_stamps": [],
            "values": []
        }

        for key, val in api_return["daily"].items():
            history_prices["time_stamps"].append(key)
            history_prices["values"].append(val)

        return history_prices

    def save_price_data(self, price_data, item_name):
        #check if directory exists
        directory = 'data/' + item_name
        if not os.path.exists(directory):
            os.makedirs(directory)

        utils.save_data(price_data, directory + '/price_history.pkl')
        # priceHistory.tofile('pastPrices/' + itemName + '.csv', sep = ',')

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

