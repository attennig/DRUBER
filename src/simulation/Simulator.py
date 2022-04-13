from math import sqrt, ceil, floor
import matplotlib.pyplot as plt
import json
import os
from src.config import *
from src.entities.Station import Station
from src.entities.Drone import Drone
from src.entities.Delivery import Delivery
from src.routing.SchedulerMILP import SchedulerMILP
from src.routing.Greedy import Greedy
from src.routing.GreedySWAP import GreedySWAP
from src.routing.LocalSearch import LocalSearch
from src.routing.Schedule import Schedule
class Simulator:
    def __init__(self, seed: int, size: int, out_path: str):
        print(f"Constructor : \n\tsimulation seed: {seed}\n\tsimulation size: {size}\n\toutput path: {out_path}")
        self.seed = seed
        self.size = size

        # Data folder
        self.outFOLDER = f"{out_path}/{size}/{seed}"
        print(f"\tdata folder {self.outFOLDER}")

        if not os.path.exists(self.outFOLDER):
            os.makedirs(self.outFOLDER)

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

        # Metrics
        self.completion_time = 0
        self.execution_time = 0

    def computeEdges(self):
        for i in self.stations.keys():
            for j in self.stations.keys():
                if i == j: continue
                if self.cost(i, j, 0) < 1:
                    #print(f"cost {i}-{j} with no parcel is {self.cost(i, j, 0)} and takes {self.time(i,j)} seconds")
                    #for d in self.deliveries.keys():
                    #    print(f"cost {i}-{j} with parcel {d} ({self.deliveries[d].weight}kg) is {self.cost(i, j, self.deliveries[d].weight)}")
                    self.edges.add((i, j))

    def generateRandomScenario(self):
        from src.simulation.RandomGenerator import RandomGenerator
        G = RandomGenerator(self)
        try:
            nu = ceil(self.size * DRONES_RATE)
            nd = ceil(self.size * DELIVERIES_RATE)
            ns = self.size - nu - nd
            print(f"{self.size} = {ns} + {nu} + {nd}")
            assert self.size == ns + nu + nd
            G.generateRandomInstance(ns, nu, nd)
        except Exception as e:
            print(e)
        G.saveInstance()
        self.computeEdges()

    def loadScenario(self):
        print(f"\tloading data from {self.outFOLDER}")

        #config_file = self.outFOLDER + "/config.json"
        data_file = self.outFOLDER + "/in.json"
        #with open(config_file) as file_in:
        #    config = json.load(file_in)
        #    assert config["AoI_SIZE"] == AoI_SIZE
        #    assert config["DRONE_SPEED"] == DRONE_SPEED
        #    assert config["DRONE_MAX_PAYLOAD"] == DRONE_MAX_PAYLOAD
        #    assert config["MIN_DISTANCE"] == MIN_DISTANCE
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

            #parameters = out['parameters']

            #self.num_activities = parameters["num_activities"]
            #self.path_len = parameters["path_len"]


            self.computeEdges()

    def run(self, algo, method=None):
        self.outAlgoFOLDER = f"{self.outFOLDER}/{algo}"
        if not os.path.exists(self.outAlgoFOLDER): os.mkdir(self.outAlgoFOLDER)
        if algo == "MILP":
            # MILP Solver
            OPT = SchedulerMILP(self, method)
        if algo == "GREEDY":
            OPT = Greedy(self)
        #if algo == "GREEDYSWAPS":
        #    OPT = GreedySWAP(self)
        if algo == "LOCALSEARCH-HC":
            OPT = LocalSearch(self, "HC")
        if algo == "LOCALSEARCH-LB":
            OPT = LocalSearch(self, "LB")
        if algo == "LOCALSEARCH-BFSOPT":
            OPT = LocalSearch(self, "BFSOPT")

        OPT.setupProblem()
        solution = OPT.solveProblem()
        if solution is not None:
            self.completion_time = solution.getCompletionTime()
            self.execution_time = OPT.exec_time
            if algo == "MILP":
                self.num_variables = OPT.model.NumVars
                self.num_constraints = OPT.model.NumConstrs
        return solution


    def saveSolution(self, solution: Schedule):
        if not os.path.exists(self.outAlgoFOLDER): os.mkdir(self.outAlgoFOLDER)
        schedule_file = f"{self.outAlgoFOLDER}/schedule.json"
        print(f"\tSaving solution in {schedule_file}")

        schedule = {}
        for u in self.drones.keys():
            schedule[u] = [action.getDICT() for action in solution.plan[u]]
        #schedule["Parameters"] = {"K": self.OPT.K, "P": self.OPT.P}
        with open(schedule_file, "w") as file_out:
            json.dump(schedule, file_out)

        map = self.getSolutionMap(solution)  # seve as map.png
        map.savefig(f"{self.outAlgoFOLDER}/map_out.png")

        metrics_file = f"{self.outAlgoFOLDER}/metrics.json"

        metrics = {"completion_time": self.completion_time,
                   "execution_time": self.execution_time}

        #metrics["MILP"] = {"NumVars": self.OPT.model.NumVars,
        #                   "NumConstrs": self.OPT.model.NumConstrs,
        #                   "RunTime": self.OPT.model.RunTime}

        with open(metrics_file, "w") as file_out:
            json.dump(metrics, file_out)

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

    def getSolutionMap(self, solution: Schedule):
        plt.clf()
        plt.subplots_adjust(bottom=0.05*(ceil(len(self.drones)/6) + ceil(len(self.deliveries)/5)))
        plt.xlim(0,AoI_SIZE)
        plt.xlabel('x')
        plt.ylim(0,AoI_SIZE)
        plt.ylabel('y')
        for s in self.stations.keys():
            plt.scatter(self.stations[s].x, self.stations[s].y, c="green", marker="s", s=200,  zorder=1)
            plt.text(self.stations[s].x, self.stations[s].y+0.3, f"{s}", c="red")
        txt = "Drones: "
        for u in self.drones.keys():
            plt.scatter(self.drones[u].home.x, self.drones[u].home.y, c="yellow", marker="3", s=100, zorder=2)
            #plt.text(self.drones[u].home.x+0.3, self.drones[u].home.y-0.3, f"{u}", c="black")
            txt += f"u{u} in s{self.drones[u].home.ID}; "
            if u % 6 == 0: txt += "\n"
            for action in solution.plan[u]:
                x_edges = [self.stations[action.x].x, self.stations[action.y].x]
                y_edges = [self.stations[action.x].y, self.stations[action.y].y]
                if action.a == 0: plt.plot(x_edges, y_edges, c="green", zorder=0)
                else: plt.plot(x_edges, y_edges, c="red", zorder=0)
        txt += "\nDeliveries: "
        for d in self.deliveries.keys():
            plt.scatter(self.deliveries[d].src.x, self.deliveries[d].src.y, c="cyan", s=20, marker="o", zorder=3)
            #plt.text(self.deliveries[d].src.x-0.5, self.deliveries[d].src.y-0.5, f"{d}:{self.deliveries[d].src.ID}->{self.deliveries[d].dst.ID}", c="brown")
            txt += f"{d}:{self.deliveries[d].src.ID}->{self.deliveries[d].dst.ID}; "
            if d % 5 == 0: txt += "\n"
        plt.figtext(0.03, 0.01, txt,  ha='left', fontsize=12)
        return plt