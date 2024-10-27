import json 
import requests
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
import utils
from PIL import Image

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

        self.osrs_api_headers = {
            'User-Agent': 'OSRS flipping Assitant',
            'From': '@thespanishinquisition6694 on Discord'  # This is another valid field
        }

    def create_json_file(self, itemName):
        baseDir = "items/"

        os.makedirs(baseDir + itemName, exist_ok=True)

        temp = '{ "low price alert":0, "high price alert":0, "last update date":"0"}'

        with open('items/' + itemName + '/trackData.json', 'w') as outfile:
            outfile.write(temp)

    def get_historical_data(self, itemId):

        #base_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"

        base_url = "https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=24h&id="

        #end_url = str(itemId) + ".json"
        end_url = str(itemId)

        request_url = base_url + end_url

        api_return = requests.get(request_url, headers = self.osrs_api_headers).json()

        history_prices = {
            "time_stamps": [],
            "values": []
        }

        for data in api_return["data"]:
            history_prices["time_stamps"].append(data["timestamp"])
            history_prices["values"].append(data["avgHighPrice"])

        return history_prices
    
    def get_item_icon(self, item_name):

        # Check if the item icon is already downloaded
        file = 'data/' + item_name + '/icon.png'
        if os.path.isfile(file):
            # Load png file and return
            return Image.open(file)
        
        # Get item id
        item_id = self.custom_items[item_name]

        base_url = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="
        end_url = str(item_id)
        request_url = base_url + end_url

        api_return = requests.get(request_url).json()
        icon_url = api_return["item"]["icon_large"]     # Or can just use icon?
        item_icon = requests.get(icon_url)

        if item_icon.status_code == 200:
            # Open the file in binary write mode and write the content of the response to it
            with open(file, 'wb') as f:
                f.write(item_icon.content)
            print("Image downloaded successfully!")
        else:
            print("Failed to download image. Status code:", item_icon.status_code)

        return Image.open(file)

    def save_price_data(self, price_data, item_name):
        #check if directory exists
        directory = 'data/' + item_name
        if not os.path.exists(directory):
            os.makedirs(directory)

        utils.save_data(price_data, directory + '/price_history.pkl')