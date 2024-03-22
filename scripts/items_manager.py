import json 
import requests
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
import utils

@dataclass
class Item():
    name: str
    id: int

class ItemsManager():

    def __init__(self):

        # Check if custom_items.json exists
        if not os.path.exists('json/custom_items.json'):
            utils.create_custom_item_ids_file()
        
        self.custom_items = json.load(open('json/custom_items.json'))

        print(self.custom_items)

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