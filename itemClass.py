
class item():
    def __init__(self, name, id, price):
        self.name = name
        self.id = id
        self.price = price

        self.highPriceAlert = False
        self.lowPriceAlert = False
        self.highPrice = 0
        self.lowPrice = 0

    def __str__(self):
        return "Item Name: " + self.name + " Item ID: " + str(self.id) + " Item Price: " + str(self.price)

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getPrice(self):
        return self.price

    def getTimestamp(self):
        return self.timestamp

    def setName(self, name):
        self.name = name

    def setId(self, id):
        self.id = id

    def setPrice(self, price):
        self.price = price