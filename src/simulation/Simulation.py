from math import sqrt, ceil
from typing import Callable
import matplotlib.pyplot as plt
import json
from src.config import *
from src.entities.Station import Station
from src.entities.Drone import Drone
from src.entities.Delivery import Delivery
from src.routing.SchedulerMILP import SchedulerMILP

class Simulation:
    def __init__(self, name: str):
        print(f"Constructor : simularion name = {name}")
        # Input Output folders
        self.inFOLDER = IN_FOLDER + "/" + name
        print(f"input folder {self.inFOLDER}")
        # Output folder
        self.outFOLDER = OUT_FOLDER + "/" + name
        print(f"output folder {self.outFOLDER}")

        # Entities
        self.stations = {}
        self.drones = {}
        self.deliveries = {}
        self.edges = set()
        # Drone flight behaviour
        # Euclidean distance between two stations given their IDs
        self.dist2D = lambda i, j: sqrt((self.stations[i].x - self.stations[j].x) ** 2 + (self.stations[i].y - self.stations[j].y) ** 2)
        self.cost = lambda i, j, w:  self.dist2D(i,j) * self.unitcost(w)
        self.unitcost = lambda w: UNIT_CONSUMPTION + ALPHA*w
        self.time = lambda i,j: self.dist2D(i,j) / DRONE_SPEED
        self.swap_time = SWAP_TIME
        self.horizon = HORIZON
        # MILP Solver
        self.OPT = SchedulerMILP(self)
        self.schedule = {}

    def computeEdges(self):
        for i in self.stations.keys():
            for j in self.stations.keys():
                if i == j: continue
                if self.cost(i, j, 0) < 1:
                    self.edges.add((i, j))

    def loadScenario(self):
        print(f"\tloading data from {self.inFOLDER}")

        config_file = self.inFOLDER+"/config.json"
        data_file = self.inFOLDER+"/in.json"
        with open(config_file) as file_in:
            config = json.load(file_in)
            assert config["SIMULATION_SEED"] == SIMULATION_SEED
            assert config["AoI_SIZE"] == AoI_SIZE
            assert config["DRONE_SPEED"] == DRONE_SPEED
            assert config["DRONE_MAX_PAYLOAD"] == DRONE_MAX_PAYLOAD
            assert config["MIN_DISTANCE"] == MIN_DISTANCE
        with open(data_file) as file_in:
            data = json.load(file_in)
            entities = data['entities']
            for s in entities['stations']:
                info = entities['stations'][s]
                self.stations[int(s)] = Station(int(s), float(info['x']), float(info['y']), int(info['capacity']))

            for d in entities['deliveries']:
                info = entities['deliveries'][d]
                src = self.stations[int(info['src'])]
                dst = self.stations[int(info['dst'])]
                self.deliveries[int(d)] = Delivery(int(d), src, dst, float(info['weight']))

            for u in entities['drones']:
                info = entities['drones'][u]
                home = self.stations[int(info['home'])]
                self.drones[int(u)] = Drone(int(u), home)

            parameters = data['parameters']
            self.num_activities = parameters["num_activities"]
            self.path_len = parameters["path_len"]


            self.computeEdges()


    def computeSchedule(self):
        print(f"\t Computing drone-delivery schedule")

        self.OPT.setupMILP(self.num_activities, self.path_len)
        self.OPT.saveMILP()
        self.OPT.solveMILP()
        if self.OPT.model.getAttr('Status') == 3:
            self.OPT.model.computeIIS()
            raise Exception(f"Model is INFEASIBLE\n{self.OPT.getISSConstrs() }")
            return
        self.OPT.extractSolution()
        self.OPT.printSolution()

    def saveSolution(self):
        schedule_file = self.outFOLDER + "/schedule.json"
        schedule = {}
        for u in self.drones.keys():
            schedule[u] = self.drones[u].schedule
        schedule["Parameters"] = {"K": self.OPT.K, "P": self.OPT.P}
        with open(schedule_file, "w") as file_out:
            json.dump(schedule, file_out)
        metrics_file = self.outFOLDER + "/metrics.json"
        metrics = {}
        metrics["MILP"] = {"NumVars": self.OPT.model.NumVars,
                           "NumConstrs": self.OPT.model.NumConstrs,
                           "RunTime": self.OPT.model.RunTime}

        print(metrics)
        with open(metrics_file, "w") as file_out:
            json.dump(metrics, file_out)

    def printStatus(self):
        print(f"The system has a total of {len(self.stations)} stations")
        for key in self.stations:
            self.stations[key].printInfo()
        print(f"The system has a total of {len(self.drones)} drones")
        for key in self.drones:
            self.drones[key].printInfo()
        print(f"The system has a total of {len(self.deliveries)} deliveries")
        for key in self.deliveries:
            self.deliveries[key].printInfo()

    def getMap(self):
        plt.clf()
        plt.subplots_adjust(bottom=0.05*(ceil(len(self.drones)/6) + ceil(len(self.deliveries)/5)))
        plt.xlim(0,AoI_SIZE)
        plt.xlabel('x')
        plt.ylim(0,AoI_SIZE)
        plt.ylabel('y')

        for i,j in self.edges:
            if i>j:
                x_edges = [self.stations[i].x, self.stations[j].x]
                y_edges = [self.stations[i].y, self.stations[j].y]
                plt.plot(x_edges,y_edges, c="grey", zorder=0)
                plt.text(0.5*(self.stations[i].x+self.stations[j].x),0.5*(self.stations[i].y+self.stations[j].y), f"{ceil(self.dist2D(i, j))}", c="gray", rotation=90*abs(self.stations[i].y-self.stations[j].y)/self.dist2D(i, j))

        for s in self.stations.keys():
            plt.scatter(self.stations[s].x, self.stations[s].y, c="green", marker="s", s=200,  zorder=1)
            plt.text(self.stations[s].x, self.stations[s].y+0.3, f"{s}", c="red")
        txt = "Drones: "
        for u in self.drones.keys():
            plt.scatter(self.drones[u].home.x, self.drones[u].home.y, c="yellow", marker="3", s=100, zorder=2)
            #plt.text(self.drones[u].home.x+0.3, self.drones[u].home.y-0.3, f"{u}", c="black")
            txt += f"u{u} in s{self.drones[u].home.ID}; "
            if u % 6 == 0: txt += "\n"
        txt += "\nDeliveries: "
        for d in self.deliveries.keys():
            plt.scatter(self.deliveries[d].src.x, self.deliveries[d].src.y, c="cyan", s=20, marker="o", zorder=3)
            #plt.text(self.deliveries[d].src.x-0.5, self.deliveries[d].src.y-0.5, f"{d}:{self.deliveries[d].src.ID}->{self.deliveries[d].dst.ID}", c="brown")
            txt += f"{d}:{self.deliveries[d].src.ID}->{self.deliveries[d].dst.ID}; "
            if d % 5 == 0: txt += "\n"
        plt.figtext(0.03, 0.01, txt,  ha='left', fontsize=12)
        return plt
