from src.entities.Drone import *
from src.entities.Delivery import *
from src.entities.WayStation import *
from src.routing.CentralizedDeliveryAssignment import *
from src.drawing.Draw import *
import json
from math import sqrt
from typing import Callable

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

        for v in self.OPT.model.getVars():
            self.solution[v.varName] = v.x
        with open(DATAPATH, "w") as file_out:
            json.dump(self.solution, file_out)

    def drawSolution(self):
        drawingObj = Draw(self)
        for t in self.T:
            #print(f"at time {t}")
            for dID in self.deliveries.keys():
                #print(f"delivery {dID}")
                for wID in self.wayStations.keys():
                    if self.solution[f"x_{dID},{wID},{t}"] == 1:
                        #print(f"is in station {wID}")
                        self.deliveries[dID].updateStation(self.wayStations[wID])
            for uID in self.drones.keys():
                #print(f"drone {uID}")

                for e in self.edges:
                    if t == self.T[-1] and self.solution[f"e_{uID},{e[0]},{e[1]},{t-1}"] == 1:
                        #print(f"is in station {e[1]}")
                        self.drones[uID].updateStation(self.wayStations[e[1]])
                    elif t < self.T[-1] and self.solution[f"e_{uID},{e[0]},{e[1]},{t}"] == 1:
                        #print(f"is in station {e[0]}")
                        self.drones[uID].updateStation(self.wayStations[e[0]])
                if t < self.T[-1]:
                    if self.solution[f"gamma_{uID},{t}"]:
                        #print(f"and it is recharging")
                        self.drones[uID].isRecharging = True
                    else:
                        #print(f"and it is not recharging")
                        self.drones[uID].isRecharging = False
            drawingObj.drawEnvironment(self, t)
