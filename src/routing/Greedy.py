import networkx as nx
from src.routing.PathPlanner import *

class Greedy(PathPlanner):
    def __init__(self, sim):
        print("\tinitializing Greedy Solver")
        PathPlanner.__init__(self, sim)


    def solveProblem(self):
        print("GREEDY ALGO")
        QUICKEST_PATHS = {d: self.computeQuickestPath(self.simulation.deliveries[d].src.ID, self.simulation.deliveries[d].dst.ID, d, self.simulation.deliveries[d].weight) for d in self.simulation.deliveries.keys()}
        LINK_PATHS = {}
        X = {u: self.simulation.drones[u].home.ID for u in self.simulation.drones.keys()}


        start_time = time.time()
        while QUICKEST_PATHS:
            min = HORIZON
            min_d, min_u = -1, -1
            for u in self.simulation.drones.keys():
                #print(f"uav {u} from {X[u]} ")
                if len(self.simulation.drones[u].schedule) == 0:
                    tau_u = 0
                else:
                    tau_u = self.simulation.drones[u].schedule[-1].tau

                for d in QUICKEST_PATHS.keys():
                    #print(f"delivery {d} from {self.simulation.deliveries[d].src.ID} to {self.simulation.deliveries[d].dst.ID}")
                    LINK_PATHS[f"{u},{d}"] = self.computeQuickestPath(X[u], self.simulation.deliveries[d].src.ID, 0, 0)
                    time_link = sum([self.simulation.time(p.x, p.y) for p in LINK_PATHS[f"{u},{d}"]])

                    pick_up_time = tau_u + time_link
                    time_path = sum([self.simulation.time(p.x, p.y) for p in QUICKEST_PATHS[d]])
                    compeltion_time = pick_up_time + time_path

                    #print(f"time of path from {X[u]} to {self.simulation.deliveries[d].src.ID} is {time_link}")
                    #print(f"time of path from {self.simulation.deliveries[d].src.ID} to {self.simulation.deliveries[d].dst.ID} is {time_path}")
                    #print(f"thus, completion time is {compeltion_time}")
                    #print(min)

                    if compeltion_time < min or (min_u == -1 and min_d == -1):
                        min = compeltion_time
                        min_u = u
                        min_d = d
            print(f"{min_d} assigned to {min_u} with completion_time {min}")

            update_time_pos = len(self.simulation.drones[min_u].schedule) - 1
            self.simulation.drones[min_u].schedule += LINK_PATHS[f"{min_u},{min_d}"] + QUICKEST_PATHS[min_d]
            self.updateTimes(min_u, update_time_pos)
            print(f"{self.simulation.drones[min_u].schedule[-1].tau}, {min}")
            assert round(self.simulation.drones[min_u].schedule[-1].tau) == round(min)

            X[min_u] = self.simulation.drones[min_u].schedule[-1].y
            QUICKEST_PATHS.pop(min_d)

        self.addSwaps()
        self.exec_time = time.time() - start_time
        print(f"exec time : {self.exec_time}")
        return True

    def addSwaps(self):
        for u in self.simulation.drones.keys():
            print(f"uav :{u}")
            SOC = self.simulation.drones[u].SoC
            schedule = self.simulation.drones[u].schedule
            i = 0
            while i < len(schedule):
                print(f"soc = {SOC}")
                w = 0
                if schedule[i].a in self.simulation.deliveries.keys():
                    w = self.simulation.deliveries[schedule[i].a].weight
                print(f"{SOC} - {self.simulation.cost(schedule[i].x,schedule[i].y,w)}")
                if SOC - self.simulation.cost(schedule[i].x,schedule[i].y,w) < 0:
                    print(f"adding swap {u}, {i}:{schedule[:i]} |SWAP| { schedule[i:]}")
                    schedule = schedule[:i] + \
                               [DroneAction(schedule[i].x, schedule[i].x, -1, schedule[i-1].tau + SWAP_TIME)] + \
                               schedule[i:]
                    SOC = 1
                    i += 1

                SOC -= self.simulation.cost(schedule[i].x, schedule[i].y, w)
                print(f"new soc = {SOC}")
                i += 1

            self.simulation.drones[u].schedule = schedule
            self.updateTimes(u, 0)



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

    def computeQuickestPath(self, src: int, dst: int, a: int, w:float):
        self.updateGraphWeights(w)
        path = nx.shortest_path(self.G, source=src, target=dst)
        #print(f"from {src} to {dst} the quickest path is: {path}")
        schedule = []
        for i in range(len(path)-1):
            x = path[i]
            y = path[i+1]
            action = DroneAction(x,y,a,0)
            schedule.append(action)
            #print(action)
        if a == 0: return schedule

        for i in range(len(schedule)):
            if i > 0: schedule[i].pred = schedule[i-1]
            if i + 1 < len(schedule): schedule[i].succ = schedule[i+1]
        return schedule

    def computeActionTime(self, action: DroneAction):
        if action.a == -1:
            return SWAP_TIME
        else:
            return self.simulation.time(action.x, action.y)
