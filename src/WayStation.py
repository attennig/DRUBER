class WayStation:
    def __init__(self, ID):
        #self.SIMULATION = sim
        assert type(ID) == int
        self.ID = ID

    def printInfo(self):
        print(f"way station ID: {self.ID}")