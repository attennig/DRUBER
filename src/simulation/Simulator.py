from math import sqrt, ceil, floor
import matplotlib.pyplot as plt
import json
import os
from time import process_time
from src.config import *
from src.entities.Station import Station
from src.entities.Drone import Drone
from src.entities.Delivery import Delivery
from src.routing.SchedulerMILP import SchedulerMILP
from src.routing.Greedy import Greedy
from src.routing.LocalSearch import LocalSearch
from src.routing.Schedule import Schedule
from src.routing.DroneAction import DroneAction

class Simulator:
    def __init__(self, seed: int, n_stations: int, n_deliveries: int, n_drones:int, in_path: str, out_path=""):
        print(f"Constructor : \n\tsimulation seed: {seed}\n\toutput path: {out_path}")
        self.seed = seed
        self.n_stations = n_stations
        self.n_deliveries = n_deliveries
        self.n_drones = n_drones
        # Data folder
        self.inFOLDER = f"{in_path}"
        self.outFOLDER = f"{out_path}/S{n_stations}D{n_deliveries}U{n_drones}/{seed}"
        print(f"\tinput data folder {self.inFOLDER}\n\toutput data folder {self.outFOLDER}")

        #if not os.path.exists(self.outFOLDER):
        #    os.makedirs(self.outFOLDER)

        # Entities
        self.stations = {}
        self.drones = {}
        self.deliveries = {}
        self.edges = set()

        # Drone flight behaviour
        # Euclidean distance between two stations given their IDs
        self.dist2D = lambda i, j: 2*ALTITUDE + sqrt((self.stations[i].x - self.stations[j].x) ** 2 + (self.stations[i].y - self.stations[j].y) ** 2)
        self.cost = lambda i, j, w:  self.time(i,j) * self.unitcost(w)
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
            G.generateRandomInstance(self.n_stations, self.n_deliveries, self.n_drones)
        except Exception as e:
            print(e)
        G.saveInstance()
        self.computeEdges()

    def loadScenario(self):
        '''
        This method loads the input instance specified constructing the Simulator object
        :return: void
        '''
        print(f"\tloading data from {self.inFOLDER}")
        data_file = f"{self.inFOLDER}/in{self.seed}.json"
        with open(data_file) as file_in:
            data = json.load(file_in)
            entities = data['entities']
            for s in range(1, self.n_stations+1): #entities['stations']:
                info = entities['stations'][str(s)]
                self.stations[int(s)] = Station(int(s), float(info['x']), float(info['y']), int(info['capacity']))

            for d in range(1, self.n_deliveries+1): #entities['deliveries']:
                info = entities['deliveries'][str(d)]
                src = self.stations[int(info['src'])]
                dst = self.stations[int(info['dst'])]
                self.deliveries[int(d)] = Delivery(int(d), src, dst, float(info['weight']))

            for u in range(1, self.n_drones+1): #entities['drones']:
                info = entities['drones'][str(u)]
                home = self.stations[int(info['home'])]
                self.drones[int(u)] = Drone(int(u), home)
            self.computeEdges()

    def loadSolution(self, algo, method):
        '''
        This method is used to load solutions and metrics previously computed.
        :param algo: algorithm name used to compute the solution.
        :param method: algorithm method, if applicable.
        :return: Schedule object containing the solution
        '''
        print(f"\tloading data from {self.outFOLDER}")
        if method is None: data_path = f"{self.outFOLDER}/{algo}"
        else: data_path = f"{self.outFOLDER}/{algo}-{method}"

        schedule_file = f"{data_path}/schedule.json"
        metric_file = f"{data_path}/metrics.json"
        with open(schedule_file) as file_in:
            plan = json.load(file_in)
        plan_o = {int(u) : [] for u in plan.keys()}
        for u in plan.keys():
            for action in plan[u]:
                plan_o[int(u)].append(DroneAction(action['x'], action['y'], action['a'], action['tau']))
        with open(metric_file) as file_in:
            metrics = json.load(file_in)
        self.execution_time = metrics["execution_time"]

        return Schedule(self, plan_o)

    def run(self, algo, method):
        if algo == "MILP":
            OPT = SchedulerMILP(self, method)
        if algo == "GREEDY":
            OPT = Greedy(self)
        if algo == "LOCALSEARCH":
            OPT = LocalSearch(self, method)
        OPT.setupProblem()
        t_start = process_time()
        solution = OPT.solveProblem()
        t_stop = process_time()
        self.execution_time = t_stop - t_start #OPT.exec_time
        return solution

    '''def computeMetrics(self, solution):
        self.completion_time = solution.getCompletionTime()
        self.mean_schedule_time = solution.getMeanScheduleTime()
        self.mean_flight_time = solution.getMeanFlightTime()
        self.mean_swap_time = solution.getMeanSwapTime()
        self.mean_idle_time = solution.getMeanIdleTime()
        self.mean_delivery_time = solution.getMeanDeliveryTime()
        self.mean_schedule_distance = solution.getMeanScheduleDistance()
        self.mean_schedule_energy = solution.getMeanScheduleEnergy()
        self.mean_number_swaps = solution.getMeanNumberSwaps()
        self.drone_utilization_time = solution.getDroneMeanUtilizationTime()
        self.drone_utilization = solution.getDroneUtilization()
        self.total_number_parcel_handover = solution.getTotalNumberParcelHandover()
        self.mean_number_parcel_handover = solution.getMeanNumberParceHandover()

        # if algo == "MILP":
        #    self.num_variables = OPT.model.NumVars
        #    self.num_constraints = OPT.model.NumConstrs'''

    def saveSolution(self, solution: Schedule, algo: str, method="", update_metrics=False):
        if not os.path.exists(self.outFOLDER): os.makedirs(self.outFOLDER)
        if solution is None: return
        if method is None != "": self.outAlgoFOLDER = f"{self.outFOLDER}/{algo}"
        else: self.outAlgoFOLDER = f"{self.outFOLDER}/{algo}-{method}"

        if not os.path.exists(self.outAlgoFOLDER): os.mkdir(self.outAlgoFOLDER)
        schedule_file = f"{self.outAlgoFOLDER}/schedule.json"
        print(f"\tSaving solution in {schedule_file}")

        if not update_metrics:
            print("saving schedule")
            schedule = {}
            for u in self.drones.keys():
                schedule[u] = [action.getDICT() for action in solution.plan[u]]
            #schedule["Parameters"] = {"K": self.OPT.K, "P": self.OPT.P}
            with open(schedule_file, "w") as file_out:
                json.dump(schedule, file_out)
            if MAP_FLAG:
                print("saving map")
                map = self.getSolutionMap(solution)  # seve as map.png
                map.savefig(f"{self.outAlgoFOLDER}/map_out.png")

        print("saving metrics")
        metrics_file = f"{self.outAlgoFOLDER}/metrics.json"
        #self.computeMetrics(solution)
        solution.computeAllMetrics()
        metrics = {
                    "completion_time":  solution.completion_time,
                    "mean_schedule_time":  solution.mean_schedule_time,
                    "mean_flight_time":  solution.mean_flight_time,
                    "mean_swap_time":  solution.mean_swap_time,
                    "mean_waiting_time":  solution.mean_waiting_time,
                    "mean_delivery_time":  solution.mean_delivery_time,
                    "mean_schedule_distance":  solution.mean_schedule_distance,
                    "mean_schedule_energy":  solution.mean_schedule_energy,
                    "mean_number_swaps":  solution.mean_number_swaps,
                    "drone_utilization_time": solution.drone_utilization_time,
                    "drone_utilization":  solution.drone_utilization,
                    "total_number_parcel_handover": solution.total_number_parcel_handover,
                    "mean_number_parcel_handover": solution.mean_number_parcel_handover,
                    "execution_time":  self.execution_time
        }

        #metrics["MILP"] = {"NumVars": self.OPT.model.NumVars,
        #                   "NumConstrs": self.OPT.model.NumConstrs,
        #                   "RunTime": self.OPT.model.RunTime}

        with open(metrics_file, "w") as file_out:
            json.dump(metrics, file_out)

    def getMap(self):
        PRINT_DETAILS = len(self.drones.keys()) + len(self.stations.keys()) + len(self.deliveries.keys()) < 100
        plt.clf()
        if PRINT_DETAILS: plt.subplots_adjust(bottom=0.05*(ceil(len(self.drones)/6) + ceil(len(self.deliveries)/5)))
        plt.xlim(0,AoI_SIZE)
        plt.xlabel('x')
        plt.ylim(0,AoI_SIZE)
        plt.ylabel('y')

        for i,j in self.edges:
            if i>j:
                x_edges = [self.stations[i].x, self.stations[j].x]
                y_edges = [self.stations[i].y, self.stations[j].y]
                plt.plot(x_edges,y_edges, c="grey", zorder=0)
                if PRINT_DETAILS: plt.text(0.5*(self.stations[i].x+self.stations[j].x),0.5*(self.stations[i].y+self.stations[j].y), f"{ceil(self.dist2D(i, j))}", c="gray", rotation=90*abs(self.stations[i].y-self.stations[j].y)/self.dist2D(i, j))

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
        if PRINT_DETAILS: plt.figtext(0.03, 0.01, txt,  ha='left', fontsize=12)
        return plt

    def getSolutionMap(self, solution: Schedule):
        PRINT_DETAILS = len(self.drones.keys()) + len(self.stations.keys()) + len(self.deliveries.keys()) < 100
        plt.clf()
        if PRINT_DETAILS: plt.subplots_adjust(bottom=0.05*(ceil(len(self.drones)/6) + ceil(len(self.deliveries)/5)))
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
        if PRINT_DETAILS: plt.figtext(0.03, 0.01, txt,  ha='left', fontsize=12)
        return plt