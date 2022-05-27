import networkx as nx
from src.routing.PathPlanner import *
from src.routing.Schedule import *

class Greedy(PathPlanner):
    def __init__(self, sim):
        print("\tinitializing Greedy Solver")
        PathPlanner.__init__(self, sim)


    def solveProblem(self):
        '''
        This method implements the greedy algorithm computing a feasible plan
        :return:
        '''

        P_sol = Schedule(self.simulation)
        QUICKEST_PATHS = {
            d: self.computeQuickestPath(
                d,
                self.simulation.deliveries[d].src.ID,
                self.simulation.deliveries[d].dst.ID,
                self.simulation.deliveries[d].weight
            ) for d in self.simulation.deliveries.keys()}


        while QUICKEST_PATHS:
            P_min = copy.deepcopy(P_sol)
            T_min = HORIZON
            u_min = None
            d_min = None
            #print(f"deliveries to assing : {len(QUICKEST_PATHS)}/{len(self.simulation.deliveries)}")
            for u in self.simulation.drones.keys():
                for d in QUICKEST_PATHS.keys():
                    #print(f"computing augmented schedule for assignment {d} -> {u}")

                    if len(P_sol.plan[u]) == 0:
                        last_station_u = self.simulation.drones[u].home.ID
                    else:
                        last_station_u = P_sol.plan[u][-1].y
                    L_aug = self.computeQuickestPath(None,
                                                     last_station_u,
                                                     self.simulation.deliveries[d].src.ID,
                                                     0)
                    P_aug = P_sol.augment(u, d, 0, L_aug, QUICKEST_PATHS[d])
                    T_aug = P_aug.arrival_times[d]
                    if T_aug < T_min:
                        T_min = T_aug
                        P_min = P_aug
                        u_min = u
                        d_min = d
            #print(f"{d_min} assigned to {u_min} with completion time {T_min}")
            P_sol = P_min
            QUICKEST_PATHS.pop(d_min)
        #print(P_sol)
        return P_sol


    def updateGraphWeights(self, w):
        self.G = nx.Graph()
        e = [(i, j, {'weight': self.simulation.time(i, j)}) for (i, j) in self.simulation.edges
             if self.simulation.cost(i, j, w) < 1]
        self.G.add_edges_from(e)

    def computeQuickestPath(self,d: int, src: int, dst: int, w:float):
        self.updateGraphWeights(w)
        path = nx.shortest_path(self.G, source=src, target=dst, weight='weight')
        schedule = []
        delivery = None
        if d in self.simulation.deliveries.keys(): delivery = d
        if delivery is not None: schedule = [DroneAction("load", src, src, delivery, None, None)]
        for i in range(len(path)-1):
            x = path[i]
            y = path[i+1]
            schedule.append(DroneAction("move", x, y, delivery, None, None))

        if delivery is not None: schedule.append(DroneAction("unload", dst, dst, delivery, None, None))
        return schedule

