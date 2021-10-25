from WayStation import *
from Delivery import *
from Drone import *
from CentralizedDeliveryAssignment import *
from CentralizedDeliveryAssignment2 import *
import json
from math import sqrt

class Simulation:
    def __init__(self, model = 1):
        assert model in [1,2]
        self.wayStations = {}
        self.deliveries = {}
        self.drones = {}
        self.T = []
        self.phi = {1: 1.5}
        self.maxdist = max(self.phi.values())

        if model == 1:
            self.OPT = CentralizedDeliveryAssignment(self)
        else:
            self.OPT = CentralizedDeliveryAssignment2(self)

    def showStatus(self):
        print(f"Horizon: {len(self.T)}")
        print(f"The system has a total of {len(self.wayStations)} way-stations")
        for key in self.wayStations:
            self.wayStations[key].printInfo()
        print(f"The system has a total of {len(self.drones)} drones")
        for key in self.drones:
            self.drones[key].printInfo()
        print(f"The system has a total of {len(self.deliveries)} deliveries")
        for key in self.deliveries:
            self.deliveries[key].printInfo()

    def loadScenario(self, DATAPATH):
        with open(DATAPATH) as file_in:
            data = json.load(file_in)
            H = data["Parameters"]["H"]
            self.T = [t for t in range(1,H+1)]
            for ws in data["Way-Stations"]:
                self.wayStations[int(ws["id"])] = WayStation(int(ws["id"]), float(ws["x"]), float(ws["y"]),
                                                             int(ws["capacity"]))
            for d in data["Deliveries"]:
                dsrc = self.wayStations[int(d["src"])]
                ddst = self.wayStations[int(d["dst"])]
                self.deliveries[int(d["id"])] = Delivery(int(d["id"]), dsrc, ddst, float(d["weight"]))

            for u in data["Drones"]:
                home = self.wayStations[int(u["home"])]
                self.drones[int(u["id"])] = Drone(int(u["id"]), home)

    def dist2D(self, i, j):
        return sqrt((self.wayStations[i].x-self.wayStations[j].x)**2 + (self.wayStations[i].y-self.wayStations[j].y)**2)

    def solve(self):
        self.OPT.solveMILP()
