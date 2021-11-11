from src.entities.WayStation import *

class Drone:
    def __init__(self, ID : int, homeWS : WayStation, initSoC : float = 1.0):
        assert 0 <= initSoC <= 1
        self.ID = ID
        self.homeWS = homeWS
        self.SoC = initSoC
        self.currentStation = homeWS
        self.isRecharging = False

    def updateStation(self, ws : WayStation):
        self.currentStation = ws


    def printInfo(self):
        print(f"Drone {self.ID} is initially located in way-station number {self.homeWS.ID}")
