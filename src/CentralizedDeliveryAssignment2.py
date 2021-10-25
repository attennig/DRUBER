from Simulation import *
import gurobipy as gp
from gurobipy import GRB

class CentralizedDeliveryAssignment2:
    def __init__(self, sim):
        print("create OPT using model 2")
        self.model = gp.Model("pathplanner")
        self.simulation = sim
        print(type(sim))

    def solveMILP(self):
        edges = set()
        for i in self.simulation.wayStations.keys():
            for j in self.simulation.wayStations.keys():
                if self.simulation.dist2D(i,j) < self.simulation.maxdist:
                    edges.add((i,j))

        # Variables
        deltas = {} # f"delta_{t}"
        drones_movements = {} # f"e_{u},{e[0]},{e[1]},{t}"
        deliveries_states = {} # f"x_{d},{w},{t}"
        deliveries_movements = {} # f"p_{d},{u},{t}")
        o_func_coeff = []
        for t in self.simulation.T:
            deltas[f"{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"delta_{t}")
            o_func_coeff.append((1.0,deltas[f"{t}"]))

        for u in self.simulation.drones.keys():
            for e in edges:
                for t in self.simulation.T[:-1]:
                    # e(u,e_i,e_j,t)
                    drones_movements[f"{u},{e[0]},{e[1]},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"e_{u},{e[0]},{e[1]},{t}")

        for d in self.simulation.deliveries.keys():
            for w in self.simulation.wayStations.keys():
                for t in self.simulation.T:
                    # x(d,w,t)
                    deliveries_states[f"{d},{w},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"x_{d},{w},{t}")

        for d in self.simulation.deliveries.keys():
            for u in self.simulation.drones.keys():
                for t in self.simulation.T[:-1]:
                    # p(d,u,i,j,t)
                    deliveries_movements[f"{d},{u},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"p_{d},{u},{t}")

        # Constraints
        c = 1
        #   Parcels' initial state x(d,w,1)
        t = 1
        for d in self.simulation.deliveries.keys():
            for w in self.simulation.wayStations.keys():
                if self.simulation.wayStations[w] == self.simulation.deliveries[d].src:
                    self.model.addConstr(deliveries_states[f"{d},{w},{t}"] == 1, f"c{c}_{d},{w},{t}")
                else:
                    self.model.addConstr(deliveries_states[f"{d},{w},{t}"] == 0, f"c{c}_{d},{w},{t}")
        #   Each parcel must be in a certain way station at each time
        c += 1
        # for d,t sum_w x(d,w,t) = 1
        for d in self.simulation.deliveries.keys():
            for t in self.simulation.T[1:]:
                sum = []
                for w in self.simulation.wayStations.keys():
                    sum.append((1.0, deliveries_states[f"{d},{w},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) == 1, f"c{c}_{d},{t}")
        #   All parcels must be delivered
        c += 1
        # for d sum_t x(d, d_dst, t) >= 1
        for d in self.simulation.deliveries.keys():
            sum = []
            d_dst = self.simulation.deliveries[d].dst.ID
            for t in self.simulation.T:
                sum.append((1.0, deliveries_states[f"{d},{d_dst},{t}"]))
            self.model.addConstr(gp.LinExpr(sum) >= 1, f"c{c}_{d}")
        #   Completion time
        c += 1
        # for t (1 - delta(t)) |D| - sum_{d in D} x(d,d_{dst},t) <= 0
        # |D| - |D|delta(t) - sum_{d in D} x(d,d_{dst}, t) <= 0
        # |D|  <=  |D|delta(t) + sum_{d in D} x(d,d_{dst}, t)
        for t in self.simulation.T:
            sum = [(len(self.simulation.deliveries), deltas[f"{t}"])]
            for d in self.simulation.deliveries.keys():
                d_dst = self.simulation.deliveries[d].dst.ID
                sum.append((1, deliveries_states[f"{d},{d_dst},{t}"]))
            self.model.addConstr(gp.LinExpr(sum) >= len(self.simulation.deliveries), f"c{c}_{t}")
        #   Drones' initial state for each u sum_(i,j)inE e(u,i,j,1) = 1
        c += 1
        t = 1
        for u in self.simulation.drones.keys():
            sum1 = []
            sum0 = []
            for e in edges:
                if e[0] == self.simulation.drones[u].homeWS.ID:
                    sum1.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                else:
                    sum0.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
            self.model.addConstr(gp.LinExpr(sum1) == 1, f"c{c}a_{u},{self.simulation.drones[u].homeWS.ID}")
            self.model.addConstr(gp.LinExpr(sum0) == 0, f"c{c}b_{u},{self.simulation.drones[u].homeWS.ID}")
        #   One drone action per time slot until completion
        c += 1
        # for u,t sum_(i,j)in E e(u,i,j,t) = delta(t)
        for u in self.simulation.drones.keys():
            for t in self.simulation.T[1:-1]:
                sum = []
                for e in edges:
                    sum.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) == deltas[f"{t}"], f"c{c}_{u},{t}")
        #   d can be carried at most by one drone
        c += 1
        # for d, t < T sum_u p(d,u,t) >= 1
        for d in self.simulation.deliveries.keys():
            for t in self.simulation.T[:-1]:
                sum = []
                for u in self.simulation.drones.keys():
                    sum.append((1.0, deliveries_movements[f"{d},{u},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"c{c}_{d},{t}")
        #   If d change position then it is assigned to a drone
        c += 1
        # for d, (i,j) i!=j, t < T x(d,i,t) + x(d,j,t+1) - sum_u  p(d,u,t) <= 1
        for d in self.simulation.drones.keys():
            for e in edges:
                if e[0] != e[1]:
                    for t in self.simulation.T[:-1]:
                        sum = [(1.0, deliveries_states[f"{d},{e[0]},{t}"]), (1.0, deliveries_states[f"{d},{e[1]},{t+1}"])]
                        for u in self.simulation.drones.keys():
                            sum.append((-1.0,deliveries_movements[f"{d},{u},{t}"]))
                        self.model.addConstr(gp.LinExpr(sum) <= 1, f"c{c}_{d},{e[0]},{e[1]},{t}")
        #   If d does not change position then is can't be assigned to a drone
        c += 1
        # for d, w, t < T x(d,i,t) + x(d,j,t+1) + sum_u  p(d,u,t) <= 2
        for d in self.simulation.drones.keys():
            for w in self.simulation.deliveries.keys():
                for t in self.simulation.T[:-1]:
                    sum = [(1.0, deliveries_states[f"{d},{w},{t}"]),
                           (1.0, deliveries_states[f"{d},{w},{t + 1}"])]
                    for u in self.simulation.drones.keys():
                        sum.append((1.0, deliveries_movements[f"{d},{u},{t}"]))
                    self.model.addConstr(gp.LinExpr(sum) <= 2, f"c{c}_{d},{w},{t}")

        #   for d, u, t < T , (i,j)  p(d,u,t) and x(d,i,t) and x(d,j,t+1) --> e(u,i,j,t)
        c += 1
        # for d, u, t < T , (i,j)  p(d,u,t) + x(d,i,t) + x(d,j,t+1) - e(u,i,j,t) <= 2
        for d in self.simulation.deliveries.keys():
            for u in self.simulation.drones.keys():
                for t in self.simulation.T[:-1]:
                    for e in edges:
                        if e[0] != e[1]:
                            self.model.addConstr(deliveries_movements[f"{d},{u},{t}"] +
                                                 deliveries_states[f"{d},{e[0]},{t}"] +
                                                 deliveries_states[f"{d},{e[1]},{t+1}"] -
                                                 drones_movements[f"{u},{e[0]},{e[1]},{t}"]<= 2,
                                                 f"c{c}_{d},{u},{t},{e[0]},{e[1]}")
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