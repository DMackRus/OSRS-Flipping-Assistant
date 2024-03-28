import pickle
import json
from PIL import ImageGrab
import datetime as dt

def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_data(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

def create_custom_item_ids_file():

    items = dict()

    itemIds = json.load(open('json/items-search.json'))
    tempFlipOpen = json.load(open('json/flipping_items.json'))

    for i, val in enumerate(tempFlipOpen):
        
        # Loop through itemids and find correct id number
        item_id = 0
        for j, val2 in enumerate(itemIds):
            
            if val["name"] == itemIds[val2]["name"]:
                item_id = itemIds[val2]["id"]
                break

        items[val["name"]] = item_id

    #create json file and save items
    with open('json/custom_items.json', 'w') as outfile:
        json.dump(items, outfile, default=lambda o: o.__dict__)

def capture_window(window):
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    width = window.winfo_width()
    height = window.winfo_height()    #get details about window
    takescreenshot = ImageGrab.grab(bbox=(x, y, width, height))
    takescreenshot.save("screenshot.png")

def convert_unix_to_timestamp(unix_time):
    unix_time = int(unix_time) // 1000
    date = dt.datetime.fromtimestamp(unix_time)
    formatted_date = date.strftime('%Y-%m-%d')
    return formatted_date

