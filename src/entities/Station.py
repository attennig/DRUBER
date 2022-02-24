class Station:
    def __init__(self, ID, x, y, capacity=2):
        assert type(ID) == int
        assert type(x) == float and type(x) == type(y)
        assert type(capacity) == int
        self.ID = ID
        self.x = x
        self.y = y
        self.capacity = capacity

    def printInfo(self):
        print(f"Station {self.ID} is in ({self.x},{self.y}) and has capacity {self.capacity}")

    def getAsDict(self):
        return {
            "x" : self.x,
            "y" : self.y,
            "capacity" : self.capacity
        }