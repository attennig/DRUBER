from src.entities.Drone import *
from src.entities.Delivery import *
from src.entities.WayStation import *
from src.routing.CentralizedDeliveryAssignment import *
from src.drawing.draw import *
import json
from math import sqrt

class Simulation:
    def __init__(self, n):
        self.wayStations = {}
        self.deliveries = {}
        self.drones = {}
        self.T = []
        self.n = n
        #self.phi = {1: 1.5, 2: 1}
        self.maxdist = 1.5#max(self.phi.values())
        # the battery recharge 10% per each time slot
        self.Bplus = 0.1
        # flying 1.5m distance in one time slot consumes 50% of the battery
        self.Bminus_fligth = lambda i,j: 0.5*self.dist2D(i,j)/self.maxdist
        # carrying a 5-kilo  parcel for one time-slot consumes 10% of the battery
        self.maxweigth = 5
        self.Bminus_weight = lambda w: 0.5*w/self.maxweigth

        self.OPT = CentralizedDeliveryAssignment(self)

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
        print(f"\tloading data from {DATAPATH}")
        with open(DATAPATH) as file_in:
            data = json.load(file_in)
            H = data["Parameters"]["H"]
            self.AoI_SIZE = data["Parameters"]["AoI_SIZE"]
            self.T = [t for t in range(1,H+1)]
            for ws in data["Way-Stations"]:
                self.wayStations[int(ws["id"])] = WayStation(int(ws["id"]),
                                                             float(ws["x"]),
                                                             float(ws["y"]),
                                                             int(ws["capacity"]))
            for d in data["Deliveries"]:
                dsrc = self.wayStations[int(d["src"])]
                ddst = self.wayStations[int(d["dst"])]
                self.deliveries[int(d["id"])] = Delivery(int(d["id"]),
                                                         dsrc,
                                                         ddst,
                                                         float(d["weight"]))

            for u in data["Drones"]:
                home = self.wayStations[int(u["home"])]
                self.drones[int(u["id"])] = Drone(int(u["id"]), home)

    def dist2D(self, i, j):
        assert type(i) == int and type(j) == int
        #print(f"distance between {i} and {j} is {sqrt((self.wayStations[i].x-self.wayStations[j].x)**2 + (self.wayStations[i].y-self.wayStations[j].y)**2)}")
        return sqrt((self.wayStations[i].x-self.wayStations[j].x)**2 + (self.wayStations[i].y-self.wayStations[j].y)**2)


    def solve(self):
        print(f"\tsolving Constrained Optimization Problem")
        self.OPT.solveMILP()
    def saveSolution(self, DATAPATH):
        print(f"\tsaving results in {DATAPATH}")
        solution = {}
        for v in self.OPT.model.getVars():
            solution[v.varName] = v.x
        with open(DATAPATH, "w") as file_out:
            json.dump(solution, file_out)

    def drawEnvironment(self):
        Draw(self)