from src.simulation.Simulation import *
import gurobipy as gp
from gurobipy import GRB
import time

class CentralizedDeliveryAssignment:
    def __init__(self, sim):
        print("\tinitializing MILP Solver")
        self.model = gp.Model("pathplanner")
        self.simulation = sim
        self.opt_time = 0

    def solveMILP(self):

        # Variables
        deltas = {}  # f"delta_{t}"
        drones_movements = {}  # f"e_{u},{e[0]},{e[1]},{t}"
        deliveries_states = {}  # f"x_{d},{w},{t}"
        deliveries_movements = {}  # f"p_{d},{u},{t}"
        o_func_coeff = []
        for t in self.simulation.T:
            deltas[f"{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"delta_{t}")
            o_func_coeff.append((1.0, deltas[f"{t}"]))

        for u in self.simulation.drones.keys():
            for e in self.simulation.edges:
                for t in self.simulation.T[:-1]:
                    # e(u,e_i,e_j,t)
                    drones_movements[f"{u},{e[0]},{e[1]},{t}"] = self.model.addVar(vtype=GRB.BINARY,
                                                                                   name=f"e_{u},{e[0]},{e[1]},{t}")

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

        # adding battery model
        state_of_charge = {}  # f"soc_{u},{t}")
        gamma = {}  # f"gamma_{},{}"
        for u in self.simulation.drones.keys():
            for t in self.simulation.T:
                state_of_charge[f"{u},{t}"] = self.model.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS,
                                                                name=f"soc_{u},{t}")
                if t < self.simulation.T[-1]:
                    gamma[f"{u},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"gamma_{u},{t}")
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
            for e in self.simulation.edges:
                if e[0] == self.simulation.drones[u].homeWS.ID:
                    sum1.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                else:
                    sum0.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
            self.model.addConstr(gp.LinExpr(sum1) <= 1, f"c{c}a_{u},{self.simulation.drones[u].homeWS.ID}")
            self.model.addConstr(gp.LinExpr(sum0) == 0, f"c{c}b_{u},{self.simulation.drones[u].homeWS.ID}")
        #   One drone action per time slot
        c += 1
        # for u,t sum_(i,j)in E e(u,i,j,t) = 1
        for u in self.simulation.drones.keys():
            for t in self.simulation.T[1:-1]:
                sum = []
                for e in self.simulation.edges:
                    sum.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) == 1, f"c{c}_{u},{t}")
        #   Drones move following linear and continuous paths
        c += 1
        # for u in U, i in WS t in [2,T-1] sum_(i,j) e(u,i,j,t) == sum_(k,i) e(u,k,i,t-1)
        for u in self.simulation.drones.keys():
            for i in self.simulation.wayStations.keys():
                for t in self.simulation.T[1:-1]:
                    sum = []
                    for e in self.simulation.edges:
                        if e[0] == i:
                            sum.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                        if e[1] == i:
                            sum.append((-1.0, drones_movements[f"{u},{e[0]},{e[1]},{t - 1}"]))
                    self.model.addConstr(gp.LinExpr(sum) == 0, f"c{c}_{u},{i},{t}")
        #   d can be carried at most by one drone
        c += 1
        # for d, t < T sum_u p(d,u,t) <= 1
        for d in self.simulation.deliveries.keys():
            for t in self.simulation.T[:-1]:
                sum = []
                for u in self.simulation.drones.keys():
                    sum.append((1.0, deliveries_movements[f"{d},{u},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"c{c}_{d},{t}")
        #   At most one parcel at time can be carried by each drone
        c += 1
        # for u in U, t in [T - 1] sum_{d in D} p(d, u, t) <= 1
        for u in self.simulation.drones.keys():
            for t in self.simulation.T[:-1]:
                sum = []
                for d in self.simulation.deliveries.keys():
                    sum.append((1.0, deliveries_movements[f"{d},{u},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"c{c}_{u},{t}")
        #   Linking x, p, e
        c += 1
        # for d in D, t < T, (i,j) in E with i!=j
        for d in self.simulation.deliveries.keys():
            for e in self.simulation.edges:
                if e[0] == e[1]: continue
                for t in self.simulation.T[:-1]:
                    sum = [(1.0, deliveries_states[f"{d},{e[0]},{t}"]),
                           (1.0, deliveries_states[f"{d},{e[1]},{t + 1}"])]
                    for u in self.simulation.drones.keys():
                        sum.append((-1.0, deliveries_movements[f"{d},{u},{t}"]))
                    # x(d, i, t) + x(d, j, t + 1) - sum_u p(d, u, t) <= 1
                    self.model.addConstr(gp.LinExpr(sum) <= 1,
                                         f"c{c}a_{d},{e[0]},{e[1]},{t}")
                    for u in self.simulation.drones.keys():
                        # p(d, u, t) + x(d, i, t) + x(d, j, t + 1) - e(u, i, j, t) <= 2
                        self.model.addConstr(deliveries_movements[f"{d},{u},{t}"] +
                                             deliveries_states[f"{d},{e[0]},{t}"] +
                                             deliveries_states[f"{d},{e[1]},{t + 1}"] -
                                             drones_movements[f"{u},{e[0]},{e[1]},{t}"] <= 2,
                                             f"c{c}b_{d},{u},{e[0]},{e[1]},{t}")
                        # e(u, i, j, t) + p(d, u, t) - x(d, i, t) <= 1
                        self.model.addConstr(drones_movements[f"{u},{e[0]},{e[1]},{t}"] +
                                             deliveries_movements[f"{d},{u},{t}"] -
                                             deliveries_states[f"{d},{e[0]},{t}"] <= 1,
                                             f"c{c}c_{d},{u},{e[0]},{e[1]},{t}")
                        # e(u, i, j, t) + p(d, u, t) - x(d, j, t + 1) <= 1
                        self.model.addConstr(drones_movements[f"{u},{e[0]},{e[1]},{t}"] +
                                             deliveries_movements[f"{d},{u},{t}"] -
                                             deliveries_states[f"{d},{e[1]},{t + 1}"] <= 1,
                                             f"c{c}d_{d},{u},{e[0]},{e[1]},{t}")
        #   A parcel can't move from i to j between t and t+1 if (i,j) not in E
        c += 1
        # for d in D, t < T, i, j in WS such that (i, j) not in E
        # x(d, i, t) + x(d, j, t + 1) <= 1
        for d in self.simulation.deliveries.keys():
            for t in self.simulation.T[:-1]:
                for i in self.simulation.wayStations.keys():
                    for j in self.simulation.wayStations.keys():
                        if (i, j) not in self.simulation.edges:
                            self.model.addConstr(deliveries_states[f"{d},{i},{t}"] +
                                                 deliveries_states[f"{d},{j},{t + 1}"] <= 1,
                                                 f"c{c}_{d},{i},{j},{t}")
        #    i=j a parcel cannot be in charge of a drone that is not moving
        c += 1
        # forall  d in D, u in U, t < T
        # p(d,u,t) <= 1 - sum_{(i,i) in E} e(u,i,i,t)
        for d in self.simulation.deliveries.keys():
            for u in self.simulation.drones.keys():
                for t in self.simulation.T[:-1]:
                    sum = [ (1.0, deliveries_movements[f"{d},{u},{t}"]) ] +\
                          [ (1.0, drones_movements[f"{u},{w},{w},{t}"] )
                            for w in self.simulation.wayStations.keys() ]
                    self.model.addConstr(gp.LinExpr(sum)<=1,
                                         f"c{c}_{d},{u},{t}")
        '''#   Parcels' weight - dependent consumption of drones' battery
        c += 1
        # for u in U, d in D, (i, j) in E, t in [T - 1]  dist(i,j) - phi(d_w) <= maxdist * (2 - (p(d,u,t) + e(u,i,j,t)) )
        for u in self.simulation.drones.keys():
            for d in self.simulation.deliveries.keys():
                for e in self.simulation.edges:
                    dist_e = self.simulation.dist2D(e[0],e[1])
                    for t in self.simulation.T[:-1]:
                        self.model.addConstr(
                            dist_e - self.simulation.phi[self.simulation.deliveries[d].weight] <=
                            maxdist * (2 - (deliveries_movements[f"{d},{u},{t}"] + drones_movements[f"{u},{e[0]},{e[1]},{t}"])),
                            f"c{c}_{u},{d},{e[0]},{e[1]},{t}")
        '''
        #   Way station maximum capacity (scenario 6)
        c += 1
        # t = 1, forall i in WS sum_{(i,j) \in E} \sum_{u in U} e(u,i,j,t) \le i_{cap}
        t = 1
        for i in self.simulation.wayStations.keys():
            sum = []
            for e in self.simulation.edges:
                if e[0] == i:
                    for u in self.simulation.drones.keys():
                        sum.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
            self.model.addConstr(gp.LinExpr(sum) <= self.simulation.wayStations[i].capacity,
                                 f"c{c}_{i},{t}init")

        # for t in [T-1], j in WS sum_{(i,j) \in E} \sum_{u in U} e(u,i,j,t) \le j_{cap}
        for j in self.simulation.wayStations.keys():
            for t in self.simulation.T[:-1]:
                sum = []
                for e in self.simulation.edges:
                    if e[1] == j:
                        for u in self.simulation.drones.keys():
                            sum.append((1.0, drones_movements[f"{u},{e[0]},{e[1]},{t}"]))
                self.model.addConstr(gp.LinExpr(sum) <= self.simulation.wayStations[j].capacity,
                                     f"c{c}_{j},{t}")

        # adding battery model
        #   Initial battery SoC
        c += 1
        # for u in U SoC(u,1) = u_soc
        for u in self.simulation.drones.keys():
            self.model.addConstr(state_of_charge[f"{u},{1}"] == self.simulation.drones[u].SoC,
                                 f"c{c}_{u}")
        #   Battery recharge only during waits
        c += 1
        # for u in U, t < T, gamma(u,t) < sum_{(i,i) in E} e(u,i,i,t)
        for u in self.simulation.drones.keys():
            for t in self.simulation.T[:-1]:
                sum = [(1, drones_movements[f"{u},{e[0]},{e[1]},{t}"])
                       for e in self.simulation.edges if e[0] == e[1]]
                self.model.addConstr(gamma[f"{u},{t}"] <= gp.LinExpr(sum),
                                     f"c{c}_{u},{t}")

        #   Battery SoC update
        c += 1
        # for u in U, t in [2,T] SoC(u,t) = SoC(u,t-1) - E^{-} + E^{+}
        for u in self.simulation.drones.keys():
            for t in self.simulation.T[1:]:
                Eplus = self.simulation.Bplus * gamma[f"{u},{t - 1}"]
                Eminus = gp.LinExpr(
                    [(self.simulation.Bminus_fligth(e[0], e[1]), drones_movements[f"{u},{e[0]},{e[1]},{t - 1}"])
                     for e in self.simulation.edges if e[0] != e[1]] +
                    [(self.simulation.Bminus_weight(self.simulation.deliveries[d].weight),
                      deliveries_movements[f"{d},{u},{t - 1}"])
                     for d in self.simulation.deliveries.keys()])
                self.model.addConstr(state_of_charge[f"{u},{t}"] ==
                                     state_of_charge[f"{u},{t - 1}"] +
                                     Eplus - Eminus,
                                     f"c{c}_{u},{t}")

        # Objective function
        o_func = gp.LinExpr(o_func_coeff)
        self.model.setObjective(o_func, GRB.MINIMIZE)
        # Save model in model.lp
        self.model.write("./out/model.lp")

        # Optimize model
        start = time.time()
        self.model.optimize()
        end = time.time()
        self.opt_time = end - start


