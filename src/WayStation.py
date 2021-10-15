class WayStation:
    def __init__(self, ID, x, y):
        assert type(ID) == int
        assert type(x) == float and type(x) == type(y)
        self.ID = ID
        self.x = x
        self.y = y

    def printInfo(self):
        print(f"way station ID: {self.ID}")