import networkx as nx
from src.routing.PathPlanner import *
from math import floor
class GreedySWAP(PathPlanner):
    def __init__(self, sim):
        print("\tinitializing Greedy Solver")
        PathPlanner.__init__(self, sim)

    def solveProblem(self):
        print("GREEDY with SWAPS ALGO")

        #QUICKEST_PATHS = {d: self.computeQuickestPath(self.simulation.deliveries[d].src.ID, self.simulation.deliveries[d].dst.ID, d, self.simulation.deliveries[d].weight) for d in self.simulation.deliveries.keys()}
        D = set(self.simulation.deliveries.keys())
        QUICKEST_PATHS = {}
        LINK_PATHS = {}
        X = {u: self.simulation.drones[u].home.ID for u in self.simulation.drones.keys()}
        SOC = {u: self.simulation.drones[u].SoC for u in self.simulation.drones.keys()}
        start_time = time.time()
        while D:
            min = HORIZON
            min_d, min_u = -1, -1
            min_new_soc = 1
            for u in self.simulation.drones.keys():
                #print(f"uav {u} from {X[u]} ")
                if len(self.simulation.drones[u].schedule) == 0:
                    tau_u = 0
                else:
                    tau_u = self.simulation.drones[u].schedule[-1].tau

                for d in D:
                    #print(f"delivery {d} from {self.simulation.deliveries[d].src.ID} to {self.simulation.deliveries[d].dst.ID}")
                    LINK_PATHS[f"{u},{d}"], new_soc = self.computeQuickestPath(X[u], self.simulation.deliveries[d].src.ID, 0, 0, SOC[u])
                    #print(f"{LINK_PATHS[f'{u},{d}']}, {new_soc}")
                    time_link = sum([self.computeActionTime(action) for action in LINK_PATHS[f"{u},{d}"]])
                    pick_up_time = tau_u + time_link


                    QUICKEST_PATHS[f"{u},{d}"], new_soc = self.computeQuickestPath(self.simulation.deliveries[d].src.ID, self.simulation.deliveries[d].dst.ID, d, self.simulation.deliveries[d].weight, new_soc)
                    #print(f"{QUICKEST_PATHS[f'{u},{d}']}, {new_soc}")
                    time_path = sum([self.computeActionTime(action) for action in QUICKEST_PATHS[f"{u},{d}"]])
                    completion_time = pick_up_time + time_path

                    #print(f"time of path from {X[u]} to {self.simulation.deliveries[d].src.ID} is {time_link}")
                    #print(f"time of path from {self.simulation.deliveries[d].src.ID} to {self.simulation.deliveries[d].dst.ID} is {time_path}")
                    #print(f"thus, completion time is {completion_time}")
                    #print(min)

                    if completion_time < min or (min_u == -1 and min_d == -1):
                        min = completion_time
                        min_u = u
                        min_d = d
                        min_new_soc = new_soc
            print(f"{min_d} assigned to {min_u} with completion_time {min} and remaining soc {min_new_soc}")

            update_time_pos = len(self.simulation.drones[min_u].schedule) - 1
            self.simulation.drones[min_u].schedule += LINK_PATHS[f"{min_u},{min_d}"] + QUICKEST_PATHS[f"{min_u},{min_d}"]
            self.updateTimes(min_u, update_time_pos)
            assert round(self.simulation.drones[min_u].schedule[-1].tau) == round(min)

            X[min_u] = self.simulation.drones[min_u].schedule[-1].y
            SOC[min_u] = min_new_soc
            D.remove(min_d)

        self.run_time = time.time() - start_time


    def updateTimes(self, u, i):
        # no handover greed needs to update only next
        for p in range(i,len(self.simulation.drones[u].schedule)):
            curr = self.simulation.drones[u].schedule[p]
            tau = 0
            if p > 0:
                prev = self.simulation.drones[u].schedule[p-1]
                tau = prev.tau
            curr.tau = tau + self.computeActionTime(curr)
            #self.simulation.drones[u].schedule[p].tau = tau + self.computeActionTime(curr) # self.simulation.time(curr.x, curr.y)
            if curr.a in self.simulation.deliveries.keys() and curr.y == self.simulation.deliveries[curr.a].dst.ID:
                self.simulation.deliveries[curr.a].arrival_time = curr.tau

    def updateGraphWeights(self, w):
        self.G = nx.Graph()
        #max_dist = floor(1 / self.simulation.unitcost(w))
        e = [(i, j, {'weight': self.simulation.time(i, j)}) for (i, j) in self.simulation.edges if
             self.simulation.cost(i, j, w) < 1]
        self.G.add_edges_from(e)

    def computeQuickestPath(self, src: int, dst: int, a: int, w: float, soc: float):

        self.updateGraphWeights(w)
        path = nx.shortest_path(self.G, source=src, target=dst)
        #print(f"from {src} to {dst} the quickest path is: {path}")
        schedule = []

        for i in range(len(path)-1):
            x = path[i]
            y = path[i+1]
            #print(f"energy needed: {self.simulation.cost(x,y,w)}, avail: {soc}")

            if soc - self.simulation.cost(x,y,w) < 0:
                action = DroneAction(x,x,-1,0)
                schedule.append(action)
                #print(action)
                soc = 1
            action = DroneAction(x,y,a,0)
            schedule.append(action)
            soc -= self.simulation.cost(x,y,w)

            assert soc > 0
            #print(action)

        if a == 0: return schedule, soc

        for i in range(len(schedule)):
            if i > 0: schedule[i].pred = schedule[i-1]
            if i + 1 < len(schedule): schedule[i].succ = schedule[i+1]
        return schedule, soc

    def computeActionTime(self, action: DroneAction):
        if action.a == -1:
            return SWAP_TIME
        else:
            return self.simulation.time(action.x, action.y)
