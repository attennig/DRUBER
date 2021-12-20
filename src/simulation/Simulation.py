from src.entities.Drone import *
from src.entities.Delivery import *
from src.entities.WayStation import *
from src.routing.CentralizedDeliveryAssignment import *
from src.config import *
import json
from math import sqrt, ceil
from typing import Callable
import random

class Simulation:
    def __init__(self, n):
        # Simulation number
        self.n = n
        # Entities
        self.wayStations = {}
        self.deliveries = {}
        self.drones = {}
        self.edges = set()
        # Time slots
        self.T = []
        # Parameters and functions
        self.maxdist = 1.5
        # the battery recharge 10% per each time slot
        self.Bplus = 0.1
        # flying 1.5m distance in one time slot consumes 50% of the battery
        self.Bminus_fligth = lambda i,j: 0.5*self.dist2D(i,j)/self.maxdist
        # carrying a 5-kilo  parcel for one time-slot consumes 10% of the battery
        self.maxweigth = 5
        self.Bminus_weight = lambda w: 0.5*w/self.maxweigth
        # It provides the distance between two way stations given their IDs
        self.dist2D : Callable[int, int] = lambda i, j: sqrt((self.wayStations[i].x - self.wayStations[j].x) ** 2 +
                                                                 (self.wayStations[i].y-self.wayStations[j].y) ** 2)
        # MILP solver
        self.OPT = CentralizedDeliveryAssignment(self)

        self.solution = {}



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

    def generateRandomInstance(self, N_stations, N_drones, N_deliveries, AoI_SIZE, H):
        self.AoI_SIZE = AoI_SIZE
        self.T = [t for t in range(1, H + 1)]
        possible_stations = {}
        for s in range(N_stations):
            x, y, c = random.uniform(0, AoI_SIZE), random.uniform(0, AoI_SIZE), random.randint(2,ceil(N_drones/3))
            self.wayStations[s] = WayStation(s, x, y, c)
            possible_stations[s] = c
        assert sum(possible_stations) >= N_drones
        for u in range(N_drones):
            home_idx = -1
            while home_idx < 0:
                idx = random.randint(0,N_stations - 1)
                if possible_stations[idx] > 0:
                    home_idx = idx
                    possible_stations[idx] -= 1
            self.drones[u] = Drone(u, self.wayStations[home_idx])
        for d in range(N_deliveries):
            src_idx = random.randint(0, N_stations - 1)
            dst_idx = random.randint(0, N_stations - 1)
            weight = random.uniform(MIN_PARCEL_WEIGHT, MAX_PARCEL_WEIGHT)
            self.deliveries[d] = Delivery(d,
                                          self.wayStations[src_idx],
                                          self.wayStations[dst_idx],
                                          weight)
        self.showStatus()

        for i in self.wayStations.keys():
            for j in self.wayStations.keys():
                #if i == j: continue
                # print(f"distance between {i} and {j} is {dist2D(self.stations[i].coord, self.stations[j].coord)}")
                dist = self.dist2D(i, j)
                if dist < self.maxdist:
                    self.edges.add((i, j))
                    #if dist < self.mindist:
                    #    self.mindist = dist

                # print(f"cost {self.costFunction(i,j, 2.3)}")
        print(self.edges)

    def loadScenario(self, DATAPATH: str):
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

            for i in self.wayStations.keys():
                for j in self.wayStations.keys():
                    if self.dist2D(i, j) < self.maxdist:
                        self.edges.add((i, j))



    def solve(self):
        print(f"\tsolving Constrained Optimization Problem")
        self.OPT.solveMILP()
    def saveSolution(self, DATAPATH: str):
        print(f"\tsaving results in {DATAPATH}")
        self.solution["execution_time"] = self.OPT.opt_time
        for v in self.OPT.model.getVars():
            self.solution[v.varName] = v.x
        with open(DATAPATH, "w") as file_out:
            json.dump(self.solution, file_out)

