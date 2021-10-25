from Simulation import *
import gurobipy as gp
from gurobipy import GRB

class CentralizedDeliveryAssignment:
    def __init__(self, sim):
        print("create OPT using model 1")
        self.model = gp.Model("pathplanner")
        self.simulation = sim
        print(type(sim))

    def solveMILP(self):
        edges = set()
        for i in self.simulation.wayStations.keys():
            for j in self.simulation.wayStations.keys():
                if self.simulation.dist2D(i, j) < self.simulation.maxdist:
                    edges.add((i, j))

        # Variables
        deltas = {}  # f"delta_{t}"
        drones_movements = {}  # f"e_{u},{e[0]},{e[1]},{t}"
        deliveries_states = {}  # f"x_{d},{w},{t}"
        deliveries_movements = {}  # f"p_{d},{u},{i},{j},{t}")
        o_func_coeff = []
        for t in self.simulation.T:
            deltas[f"{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"delta_{t}")
            o_func_coeff.append((1.0, deltas[f"{t}"]))

        for u in self.simulation.drones.keys():
            for e in edges:
                for t in self.simulation.T:
                    # e(u,e_i,e_j,t)
                    drones_movements[f"{u},{e[0]},{e[1]},{t}"] = self.model.addVar(vtype=GRB.BINARY,
                                                                                   name=f"e_{u},{e[0]},{e[1]},{t}")

        for d in self.simulation.deliveries.keys():
            for w in self.simulation.wayStations.keys():
                for t in self.simulation.T:
                    # x(d,w,t)
                    deliveries_states[f"{d},{w},{t}"] = self.model.addVar(vtype=GRB.BINARY,
                                                                          name=f"x_{d},{w},{t}")

        for d in self.simulation.deliveries.keys():
            for u in self.simulation.drones.keys():
                for e in edges:
                    for t in self.simulation.T:
                        # p(d,u,i,j,t)
                        deliveries_movements[f"{d},{u},{e[0]},{e[1]},{t}"] = self.model.addVar(
                            vtype=GRB.BINARY, name=f"p_{d},{u},{e[0]},{e[1]},{t}")

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
            self.model.addConstr(gp.LinExpr(sum1) == 1,
                                 f"c{c}a_{u},{self.simulation.drones[u].homeWS.ID}")
            self.model.addConstr(gp.LinExpr(sum0) == 0,
                                 f"c{c}b_{u},{self.simulation.drones[u].homeWS.ID}")
        #   One drone action per time slot
        c += 1
        # for u,t sum_(i,j)in E e(u,i,j,t) = delta(t)
        for u in self.simulation.drones.keys():
            for t in self.simulation.T[1:]:
                sum = []
                for e in edges:
                    sum.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) == 1, f"c{c}_{u},{t}")
        #   Given a delivery request, its parcel can be carried at most by one drone at each time step
        c += 1
        # for d,t sum_u sum_(ij) p(d,u,i,j,t) <= 1
        for d in self.simulation.deliveries.keys():
            for t in self.simulation.T:
                sum = []
                for u in self.simulation.drones.keys():
                    for e in edges:
                        sum.append((1.0, deliveries_movements[f"{d},{u},{e[0]},{e[1]},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"c{c}_{d},{t}")

        #   Given a delivery request, its parcel can move only if carried by a drone
        c += 1
        # for d, u, (i,j), t   p(d,u,i,j,t) <= e(u,i,j,t)
        for d in self.simulation.deliveries.keys():
            for t in self.simulation.T:
                for u in self.simulation.drones.keys():
                    for e in edges:
                        self.model.addConstr(
                            deliveries_movements[f"{d},{u},{e[0]},{e[1]},{t}"] - drones_movements[
                                f"{u},{e[0]},{e[1]},{t}"] <= 0,
                            f"c{c}_{d},{u},{t},{e[0]},{e[1]}")
        #   Parcel location update:
        c += 1
        # for d, j, t  x(d,j,t) <= x(d,j,t-1) + sum_u sum_ij p(d,u,i,j,t-1)
        for d in self.simulation.deliveries.keys():
            for j in self.simulation.wayStations.keys():
                for t in self.simulation.T[1:]:
                    sum = [(1.0, deliveries_states[f"{d},{j},{t}"]), (-1.0, deliveries_states[f"{d},{j},{t - 1}"])]
                    for u in self.simulation.drones:
                        for e in edges:
                            if e[1] == j:
                                sum.append((-1.0, deliveries_movements[f"{d},{u},{e[0]},{j},{t - 1}"]))
                    self.model.addConstr(gp.LinExpr(sum) <= 0, f"c{c}_{d},{j},{t}")
        #   Drones follow linear and continuous paths
        c += 1
        # all u, (i,j), t>1 e(u,i,j,t) <= sum_(k,i) e(u,k,i,t-1)
        for u in self.simulation.drones.keys():
            for e in edges:
                for t in self.simulation.T[1:]:
                    sum = [(1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"])]
                    for e2 in [in_e for in_e in edges if in_e[1] == e[0]]:
                        sum.append((-1.0, drones_movements[f"{u},{e2[0]},{e2[1]},{t - 1}"]))
                    self.model.addConstr(gp.LinExpr(sum) <= 0, f"c{c}_{u},{e[0]},{e[1]},{t}")
        #   u can carry d from i to j only if d is already in i
        c += 1
        # all d, i, t :  x(d,i,t) >= sum_u sum_ij p
        for d in self.simulation.deliveries.keys():
            for i in self.simulation.wayStations.keys():
                for t in self.simulation.T:
                    sum = [(1.0, deliveries_states[f"{d},{i},{t}"])]
                    for u in self.simulation.drones.keys():
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


