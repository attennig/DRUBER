from WayStation import *

class Drone:
    def __init__(self, ID, homeWS):
        assert type(ID) == int
        assert type(homeWS) == WayStation
        self.ID = ID
        self.homeWS = homeWS


    def printInfo(self):
        print(f"Drone {self.ID} is initially located in way-station number {self.homeWS.ID}")
