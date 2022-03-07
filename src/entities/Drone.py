from src.simulation.Simulator import *
from src.routing.DroneAction import *
class Drone:
    def __init__(self, ID : int, home : Station, initSoC : float = 1.0):
        assert 0 <= initSoC <= 1
        self.ID = ID
        self.home = home
        self.SoC = initSoC
        self.currentStation = home
        self.isRecharging = False
        self.schedule = []

    def updateStation(self, s : Station):
        self.currentStation = s

    def printInfo(self):
        print(f"Drone {self.ID} is initially located in way-station number {self.home.ID}")

    def getAsDict(self):
        return {
            "home" : self.home.ID
        }

    def addAction(self, action: DroneAction):
        #action = self.DroneAction(x, y, a, tau)
        self.schedule.append(action)
        #return action

    def getScheduleDICT(self):
        return [action.getDICT() for action in self.schedule]


