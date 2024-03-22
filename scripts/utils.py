import pickle
import json

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
