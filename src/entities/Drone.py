from src.entities.WayStation import *

class Drone:
    def __init__(self, ID, homeWS, initSoC=1.0):
        assert type(ID) == int
        assert type(homeWS) == WayStation
        assert type(initSoC) == float and 0 <= initSoC <= 1
        self.ID = ID
        self.homeWS = homeWS
        self.SoC = initSoC


    def printInfo(self):
        print(f"Drone {self.ID} is initially located in way-station number {self.homeWS.ID}")
