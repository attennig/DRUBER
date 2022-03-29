import networkx as nx
from src.routing.PathPlanner import *
from src.routing.Schedule import *

class Greedy(PathPlanner):
    def __init__(self, sim):
        print("\tinitializing Greedy Solver")
        PathPlanner.__init__(self, sim)


    def solveProblem(self):
        QUICKEST_PATHS = {d: self.computeQuickestPath(self.simulation.deliveries[d].src.ID, self.simulation.deliveries[d].dst.ID, d, self.simulation.deliveries[d].weight) for d in self.simulation.deliveries.keys()}
        LINK_PATHS = {}
        X = {u: self.simulation.drones[u].home.ID for u in self.simulation.drones.keys()}
        start_time = time.time()
        schedule = Schedule(self.simulation)
        while QUICKEST_PATHS:
            min = HORIZON
            min_d, min_u = -1, -1
            for u in self.simulation.drones.keys():
                if len(schedule.plan[u]) == 0:
                    tau_u = 0
                else:
                    tau_u = schedule.plan[u][-1].tau

                for d in QUICKEST_PATHS.keys():
                    LINK_PATHS[f"{u},{d}"] = self.computeQuickestPath(X[u], self.simulation.deliveries[d].src.ID, 0, 0)
                    time_link = sum([self.simulation.time(p.x, p.y) for p in LINK_PATHS[f"{u},{d}"]])

                    pick_up_time = tau_u + time_link
                    time_path = sum([self.simulation.time(p.x, p.y) for p in QUICKEST_PATHS[d]])
                    compeltion_time = pick_up_time + time_path

                    if compeltion_time < min or (min_u == -1 and min_d == -1):
                        min = compeltion_time
                        min_u = u
                        min_d = d

            update_time_pos = len(schedule.plan[min_u]) - 1
            schedule.plan[min_u] += LINK_PATHS[f"{min_u},{min_d}"] + QUICKEST_PATHS[min_d]
            schedule.updateTimes(min_u, update_time_pos)
            assert round(schedule.plan[min_u][-1].tau) == round(min)

            X[min_u] = schedule.plan[min_u][-1].y
            QUICKEST_PATHS.pop(min_d)

        schedule.addBatterySwaps()

        self.exec_time = time.time() - start_time
        return schedule




    def updateGraphWeights(self, w):
        self.G = nx.Graph()
        #max_dist = floor(1 / self.simulation.unitcost(w))
        e = [(i, j, {'weight': self.simulation.time(i, j)}) for (i, j) in self.simulation.edges if
             self.simulation.cost(i, j, w) < 1]
        self.G.add_edges_from(e)

    def computeQuickestPath(self, src: int, dst: int, a: int, w:float):
        self.updateGraphWeights(w)
        path = nx.shortest_path(self.G, source=src, target=dst, weight='weight')
        schedule = []
        for i in range(len(path)-1):
            x = path[i]
            y = path[i+1]
            action = DroneAction(x,y,a,0)
            schedule.append(action)
        if a == 0: return schedule

        for i in range(len(schedule)):
            if i > 0: schedule[i].pred = schedule[i-1]
            if i + 1 < len(schedule): schedule[i].succ = schedule[i+1]
        return schedule

