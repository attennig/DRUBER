from WayStation import *
from Delivery import *
from Drone import *
import json
import gurobipy as gp
from gurobipy import GRB
from math import sqrt

class Simulation:
    def __init__(self):
        self.wayStations = {}
        self.deliveries = {}
        self.drones = {}
        self.T = []
        self.model = gp.Model("pathplanner")
        self.phi = {1: 1.5}
        self.maxdist = max(self.phi.values())

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
        with open(DATAPATH) as file_in:
            data = json.load(file_in)
            H = data["Parameters"]["H"]
            self.T = [t for t in range(1,H+1)]
            for ws in data["Way-Stations"]:
                self.wayStations[int(ws["id"])] = WayStation(int(ws["id"]), float(ws["x"]), float(ws["y"]),
                                                             int(ws["capacity"]))
            for d in data["Deliveries"]:
                dsrc = self.wayStations[int(d["src"])]
                ddst = self.wayStations[int(d["dst"])]
                self.deliveries[int(d["id"])] = Delivery(int(d["id"]), dsrc, ddst, float(d["weight"]))

            for u in data["Drones"]:
                home = self.wayStations[int(u["home"])]
                self.drones[int(u["id"])] = Drone(int(u["id"]), home)

    def dist2D(self, i, j):
        return sqrt((self.wayStations[i].x-self.wayStations[j].x)**2 + (self.wayStations[i].y-self.wayStations[j].y)**2)

    def solveMILP(self):
        edges = set()
        for i in self.wayStations.keys():
            for j in self.wayStations.keys():
                if self.dist2D(i,j) < self.maxdist:
                    edges.add((i,j))

        # Variables
        deltas = {} # f"delta_{t}"
        drones_movements = {} # f"e_{u},{e[0]},{e[1]},{t}"
        deliveries_states = {} # f"x_{d},{w},{t}"
        deliveries_movements = {} # f"p_{d},{u},{i},{j},{t}")
        o_func_coeff = []
        for t in self.T:
            deltas[f"{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"delta_{t}")
            o_func_coeff.append((1.0,deltas[f"{t}"]))

        for u in self.drones.keys():
            for e in edges:
                for t in self.T:
                    # e(u,e_i,e_j,t)
                    drones_movements[f"{u},{e[0]},{e[1]},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"e_{u},{e[0]},{e[1]},{t}")

        for d in self.deliveries.keys():
            for w in self.wayStations.keys():
                for t in self.T:
                    # x(d,w,t)
                    deliveries_states[f"{d},{w},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"x_{d},{w},{t}")

        for d in self.deliveries.keys():
            for u in self.drones.keys():
                for e in edges:
                    for t in self.T:
                        # p(d,u,i,j,t)
                        deliveries_movements[f"{d},{u},{e[0]},{e[1]},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"p_{d},{u},{e[0]},{e[1]},{t}")

        # Constraints
        c = 1
        #   Parcels' initial state x(d,w,1)
        t = 1
        for d in self.deliveries.keys():
            for w in self.wayStations.keys():
                if self.wayStations[w] == self.deliveries[d].src:
                    self.model.addConstr(deliveries_states[f"{d},{w},{t}"] == 1, f"c{c}_{d},{w},{t}")
                else:
                    self.model.addConstr(deliveries_states[f"{d},{w},{t}"] == 0, f"c{c}_{d},{w},{t}")
        #   Each parcel must be in a certain way station at each time
        c += 1
        # for d,t sum_w x(d,w,t) = 1
        for d in self.deliveries.keys():
            for t in self.T[1:]:
                sum = []
                for w in self.wayStations.keys():
                    sum.append((1.0, deliveries_states[f"{d},{w},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) == 1, f"c{c}_{d},{t}")
        #   All parcels must be delivered
        c += 1
        # for d sum_t x(d, d_dst, t) >= 1
        for d in self.deliveries.keys():
            sum = []
            d_dst = self.deliveries[d].dst.ID
            for t in self.T:
                sum.append((1.0, deliveries_states[f"{d},{d_dst},{t}"]))
            self.model.addConstr(gp.LinExpr(sum) >= 1, f"c{c}_{d}")
        #   Completion time
        c += 1
        # for t (1 - delta(t)) |D| - sum_{d in D} x(d,d_{dst},t) <= 0
        # |D| - |D|delta(t) - sum_{d in D} x(d,d_{dst}, t) <= 0
        # |D|  <=  |D|delta(t) + sum_{d in D} x(d,d_{dst}, t)
        for t in self.T:
            sum = [(len(self.deliveries), deltas[f"{t}"])]
            for d in self.deliveries.keys():
                d_dst = self.deliveries[d].dst.ID
                sum.append((1, deliveries_states[f"{d},{d_dst},{t}"]))
            self.model.addConstr(gp.LinExpr(sum) >= len(self.deliveries), f"c{c}_{t}")
        #   Drones' initial state for each u sum_(i,j)inE e(u,i,j,1) = 1
        c += 1
        t = 1
        for u in self.drones.keys():
            sum1 = []
            sum0 = []
            for e in edges:
                if e[0] == self.drones[u].homeWS.ID:
                    sum1.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                else:
                    sum0.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
            self.model.addConstr(gp.LinExpr(sum1) == 1, f"c{c}a_{u},{self.drones[u].homeWS.ID}")
            self.model.addConstr(gp.LinExpr(sum0) == 0, f"c{c}b_{u},{self.drones[u].homeWS.ID}")
        #   One drone action per time slot
        c += 1
        # for u,t sum_(i,j)in E e(u,i,j,t) = delta(t)
        for u in self.drones.keys():
            for t in self.T[1:]:
                sum = []
                for e in edges:
                    sum.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) == 1, f"c{c}_{u},{t}")
        #   Given a delivery request, its parcel can be carried at most by one drone at each time step
        c += 1
        # for d,t sum_u sum_(ij) p(d,u,i,j,t) <= 1
        for d in self.deliveries.keys():
            for t in self.T:
                sum = []
                for u in self.drones.keys():
                    for e in edges:
                        sum.append((1.0, deliveries_movements[f"{d},{u},{e[0]},{e[1]},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"c{c}_{d},{t}")

        #   Given a delivery request, its parcel can move only if carried by a drone
        c += 1
        # for d, u, (i,j), t   p(d,u,i,j,t) <= e(u,i,j,t)
        for d in self.deliveries.keys():
            for t in self.T:
                for u in self.drones.keys():
                    for e in edges:
                        self.model.addConstr(
                            deliveries_movements[f"{d},{u},{e[0]},{e[1]},{t}"] - drones_movements[f"{u},{e[0]},{e[1]},{t}"] <= 0,
                            f"c{c}_{d},{u},{t},{e[0]},{e[1]}")
        #   Parcel location update:
        c += 1
        # for d, j, t  x(d,j,t) <= x(d,j,t-1) + sum_u sum_ij p(d,u,i,j,t-1)
        for d in self.deliveries.keys():
            for j in self.wayStations.keys():
                for t in self.T[1:]:
                    sum = [(1.0,deliveries_states[f"{d},{j},{t}"]),(-1.0,deliveries_states[f"{d},{j},{t-1}"])]
                    for u in self.drones:
                        for e in edges:
                            if e[1] == j:
                                sum.append((-1.0, deliveries_movements[f"{d},{u},{e[0]},{j},{t-1}"]))
                    self.model.addConstr(gp.LinExpr(sum) <= 0, f"c{c}_{d},{j},{t}")
        #   Drones follow linear and continuous paths
        c += 1
        # all u, (i,j), t>1 e(u,i,j,t) <= sum_(k,i) e(u,k,i,t-1)
        for u in self.drones.keys():
            for e in edges:
                for t in self.T[1:]:
                    sum = [(1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"])]
                    for e2 in [in_e for in_e in edges if in_e[1] == e[0]]:
                        sum.append((-1.0, drones_movements[f"{u},{e2[0]},{e2[1]},{t-1}"]))
                    self.model.addConstr(gp.LinExpr(sum) <= 0, f"c{c}_{u},{e[0]},{e[1]},{t}")
        #   u can carry d from i to j only if d is already in i
        c += 1
        # all d, i, t :  x(d,i,t) >= sum_u sum_ij p
        for d in self.deliveries.keys():
           for i in self.wayStations.keys():
                for t in self.T:
                    sum = [(1.0,deliveries_states[f"{d},{i},{t}"])]
                    for u in self.drones.keys():
                        for e in [edge for edge in edges if edge[0] == i]:
                            sum.append((-1.0, deliveries_movements[f"{d},{u},{e[0]},{e[1]},{t}"]))
                    self.model.addConstr(gp.LinExpr(sum) >= 0, f"c{c}_{d},{i},{t}")


        # Objective function
        o_func = gp.LinExpr(o_func_coeff)
        self.model.setObjective(o_func, GRB.MINIMIZE)
        # Save model in model.lp
        self.model.write("../out/model.lp")

        # Optimize model
        self.model.optimize()
        # Extract solution
        for v in self.model.getVars():
            print(f"{v.varName} = {v.x}")

if __name__ == "__main__":
    DATAPATH = "../data/scenario1.json"
    S = Simulation()
    S.loadScenario(DATAPATH)
    S.showStatus()
    S.solveMILP()