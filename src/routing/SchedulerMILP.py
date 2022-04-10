import gurobipy as gp
from gurobipy import GRB
import os
from src.routing.PathPlanner import *


class SchedulerMILP(PathPlanner):
    def __init__(self, sim, method):
        print("\tinitializing MILP Solver")
        PathPlanner.__init__(self, sim)
        env = gp.Env(empty=True)
        env.setParam('TimeLimit', OPT_TIME_LIMIT * 60)
        env.setParam('MemLimit', OPT_MEM_LIMIT)
        env.setParam('Method', MILP_METHODS[method])
        env.start()
        self.model = gp.Model(env=env)


    def setupProblem(self):
        print(f"\t Setting up MILP")
        #self.simulation.printStatus()

        diameter = self.computeDiameter()
        self.K = 2 * diameter +  2 * (diameter - 1)
        self.P = diameter


        '''
                        x[f"{u},{k},{i},{j}"]
                        delta[f"{u},{k}"]
                        f[f"{d},{p},{i},{j}"]
                        y[f"{u},{k},{d},{p}"]
                        gamma[f"{u},{k}"]
                        B[f"{u},{k}"]
                        CU[f"{u},{k}"]
                        CD[f"{d},{p}"]
                        CT
                        '''

        ############ Variables #############
        # BINARY : x^{u,k}_{i,j} = 1: u's k-th activity fly i -> j; 0: otherwise.
        # all u, k, (i,j)
        x = {}  # f"x_{u},{k},{i},{j}"
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for (i,j) in self.simulation.edges:
                    x[f"{u},{k},{i},{j}"] = self.model.addVar(vtype=GRB.BINARY, name=f"x_{u},{k},{i},{j}")
        # BINARY : delta^{u,k} = 1: u's k-th activity is the first flight; 0: otherwise.
        # all u, k
        delta = {}  # delta"x_{u},{k}"
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                delta[f"{u},{k}"] = self.model.addVar(vtype=GRB.BINARY, name=f"delta_{u},{k}")
        # BINARY : f^{d,p}_{i,j} = 1: d's p-th edge is i,j; 0: otherwise.
        # all d, p, (i,j)
        f = {}  # f"{d},{p},{i},{j}"
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                for (i,j) in self.simulation.edges:
                    f[f"{d},{p},{i},{j}"] = self.model.addVar(vtype=GRB.BINARY, name=f"f_{d},{p},{i},{j}")
        # BINARY : y^{u,k}_{d,p} = 1: p-th edge in d's path is assigned to u's k-th activity; 0: otherwise.
        # all d, p, u, k
        y = {} # f"y_{u},{k},{d},{p}"
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                for u in self.simulation.drones.keys():
                    for k in range(self.K):
                        y[f"{u},{k},{d},{p}"] = self.model.addVar(vtype=GRB.BINARY, name=f"y_{u},{k},{d},{p}")

        # BINARY : gamma^{u,k} = 1: u's k-th activity consists in swapping its battery; 0 otherwise.
        # all u, k
        gamma = {} # f"gamma_{u},{k}"
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                gamma[f"{u},{k}"] = self.model.addVar(vtype=GRB.BINARY, name=f"gamma_{u},{k}")

        # CONTINUOUS : B^{u,k} = u's battery State of Charge at the end of $k$-th activity.
        # all u, k
        B = {} # f"B_{u},{k}"
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                B[f"{u},{k}"] = self.model.addVar(vtype=GRB.CONTINUOUS, name=f"B_{u},{k}", lb=0, ub=1)

        # CONTINUOUS : C^{u,k} = completion time of job scheduled as u's k-th activity.
        # all u, k
        CU = {} # f"C_{u},{k}"
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                CU[f"{u},{k}"] = self.model.addVar(vtype=GRB.CONTINUOUS, name=f"C_{u},{k}")

        # CONTINUOUS : C^{d,p} = completion time of p'th edge of delivery d.
        # all u, k
        CD = {}  # f"CD_{u},{k}"
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                CD[f"{d},{p}"] = self.model.addVar(vtype=GRB.CONTINUOUS, name=f"CD_{d},{p}")

        # CONTINUOUS : C = completion time
        CT = self.model.addVar(vtype=GRB.CONTINUOUS, name="C")

        ############ Constraints #############

        # Drones’ flows

        # eq:fistflightcard = the first flight is at most one
        for u in self.simulation.drones.keys():
            sum = [(1.0, delta[f"{u},{k}"]) for k in range(self.K)]
            self.model.addConstr(gp.LinExpr(sum) <= 1, f"fistflightcard_{u}")
        # eq:firstflighdef = delta_uk is 1 the kth is the first flight
        # delta_uk >= sum_ij x_ukij - sum_k1=1...k-1 x_uk1ij
        # all u,k,
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                sum = [(-1.0, x[f"{u},{k},{i},{j}"]) for (i,j) in self.simulation.edges] + \
                      [(1.0, x[f"{u},{k1},{i},{j}"]) for (i,j) in self.simulation.edges for k1 in range(k)]
                self.model.addConstr(delta[f"{u},{k}"] + gp.LinExpr(sum) >= 0, f"firstflighdef_{u},{k}")
        # eq:trajectorystart the first flight of a drone is from its source
        # delta_uk <= sum_sigmau,j x_uksimgauj
        # all u, k
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                sum = [(-1.0, x[f"{u},{k},{i},{j}"]) for (i,j) in self.simulation.edges if i == self.simulation.drones[u].home.ID]
                self.model.addConstr(delta[f"{u},{k}"] + gp.LinExpr(sum) <= 0, f"trajectorystart_{u},{k}")


        # eq:flightprecdecessor if not first flight has a predecessor
        # x_ukij - delta_uk <= sum_si sum_k1=0..k-1 x_siuk1
        # all u, k, ij
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for (i, j) in self.simulation.edges:
                    sum = [(-1.0, x[f"{u},{k1},{s1},{s2}"]) for (s1, s2) in self.simulation.edges if s2 == i for k1 in range(k)]
                    self.model.addConstr(x[f"{u},{k},{i},{j}"] - delta[f"{u},{k}"] + gp.LinExpr(sum) <= 0, f"flightpredecessor_{u},{k},{i}-{j}")
        
        # eq:droneflow2 = flow conservation rule
        for u in self.simulation.drones.keys():
            for s in self.simulation.stations.keys():
                for k1 in range(self.K):
                    sum = []
                    for k in range(k1):
                        sum += [(1.0, x[f"{u},{k},{i},{j}"]) for (i, j) in self.simulation.edges if j == s] + \
                              [(-1.0, x[f"{u},{k},{j},{i}"]) for (j, i) in self.simulation.edges if j == s]
                    if s == self.simulation.drones[u].home.ID:
                        lb = -1
                        ub = 0
                    else:
                        lb = 0
                        ub = 1

                    self.model.addConstr(gp.LinExpr(sum) >= lb, f"droneflow2a_{u},{s},{k1}")
                    self.model.addConstr(gp.LinExpr(sum) <= ub, f"droneflow2b_{u},{s},{k1}")


        # Deliveries’ flows
        # eq:deliveryflow1 = Each path corresponds to at most one edge
        # sum_{(i,j) \in E} f^{d,p}_{i,j} <= 1
        # all d, p
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                sum = [(1.0, f[f"{d},{p},{i},{j}"]) for (i, j) in self.simulation.edges]
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"deliveryflow1_{d},{p}")

        # eq:deliveryflow3 = Each delivery path starts in delivery source and ends in delivery destination.
        # sum_p (sum_ij f^{d,p}_{i,j} - sum_ji f^{d,p}_{j,i}) = 1 j=a_d, -1 j=b_d, 0 otw
        # all d , j
        for d in self.simulation.deliveries.keys():
            for s in self.simulation.stations.keys():
                sum = []
                for p in range(self.P):

                    sum += [(1.0,f[f"{d},{p},{i},{j}"]) for (i,j) in self.simulation.edges if j == s] +\
                           [(-1.0,f[f"{d},{p},{j},{i}"]) for (j,i) in self.simulation.edges if j == s]

                if s == self.simulation.deliveries[d].src.ID:
                    kt = -1
                elif s == self.simulation.deliveries[d].dst.ID:
                    kt = 1
                else:
                    kt = 0
                self.model.addConstr(gp.LinExpr(sum) == kt, f"deliveryflow3_{d},{s}")

        # deliveryflows
        # f_dpij <= sum_s1s2 f_dp-1s1s2
        # all d, p>1, ij
        for d in self.simulation.deliveries.keys():
            for p in range(1,self.P):
                for (i, j) in self.simulation.edges:
                    sum = [(-1.0, f[f"{d},{p-1},{s1},{s2}"]) for (s1,s2) in self.simulation.edges if s2 == i]
                    self.model.addConstr( f[f"{d},{p},{i},{j}"] + gp.LinExpr(sum) <= 0, f"deliveryflows_{d},{p},{i}-{j}")


        # Delivery assignment
        # eq:ycard2 = each drone activity is assigned at most to one path's edge
        # sum_d  sum_p y^{u, k}_{d, p} <= 1
        # all  u, k
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                sum = [(1.0, y[f"{u},{k},{d},{p}"]) for d in self.simulation.deliveries.keys() for p in range(self.P)]
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"ycard2_{u},{k}")
        # eq: ycard1 = each path's edge is assigned at most to one activity.
        # sum_u sum_k y^{u, k}_d, p}<= 1
        # all d, p
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                sum = [(1.0, y[f"{u},{k},{d},{p}"]) for u in self.simulation.drones.keys() for k in range(self.K)]
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"ycard1_{d},{p}")

        # Linking variables
        # eq:linkvars1 = a path's edge is assigned to a drone's activity iff the path's edge corresponds to an actual edge.
        # sum_ij f^{d,p}_{i,j} = sum_u sum_k y^{u,k}_{d,p}
        # all d, p
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                sum = [(1.0, f[f"{d},{p},{i},{j}"]) for (i,j) in self.simulation.edges] + \
                      [(-1.0, y[f"{u},{k},{d},{p}"]) for u in self.simulation.drones.keys() for k in range(self.K)]
                self.model.addConstr(gp.LinExpr(sum) == 0, f"linkvars1_{d},{p}")
        # eq:linkvars2 = when a delivery is assigned to a drone they move consistently.
        # y^{u,k}_{d,p} + f^{d,p}_{i,j} - x^{u,k}_{i,j} <= 2
        # all u, k, d, p, ij
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for d in self.simulation.deliveries.keys():
                    for p in range(self.P):
                        for (i, j) in self.simulation.edges:
                            self.model.addConstr(y[f"{u},{k},{d},{p}"] + f[f"{d},{p},{i},{j}"] - x[f"{u},{k},{i},{j}"] <= 1, f"linkvars2_{u},{k},{d},{p},{i}-{j}")

        # Battery
        # eq:swapormove = swap or move or idle
        # \gamma^{u,k} + sum_{(i,j) \in E} x^{u,k}_{i,j} = 1
        # all u  k \in [K]
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                sum = [(1.0, gamma[f"{u},{k}"])]
                sum += [(1.0, x[f"{u},{k},{i},{j}"]) for (i, j) in self.simulation.edges]
                self.model.addConstr(gp.LinExpr(sum) <= 1, f"swapnotmove_{u},{k},")
        # eq:batterysocswap = set the battery SoC to 1 each time the drone swap its battery.
        # B^{u,k} >= \gamma^{u,k}
        # all u, k
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                self.model.addConstr(B[f"{u},{k}"] - gamma[f"{u},{k}"] >= 0, f"batterysocswap_{u},{k}")
        # eq:batteryconsumption0 = init soc
        # B^{u,-1}}{=}{\Gamma_{u}}
        # all u
        # for u in self.simulation.drones.keys():
        #    self.model.addConstr(B[f"{u},{0}"] == self.simulation.drones[u].SoC, f"batteryconsumption0_{u}")
        # eq:batteryconsumption1 = consumption if move w/o payload
        # B^{u,k} - B^{u,k-1} + sum_{(i,j) \in E} x^{u,k}_{i,j} \cdot c(i,j,0) - M\gamma^{u,k} <=  0
        # all u, k > 1

        for u in self.simulation.drones.keys():
            for k in range(self.K):
                sum = []
                if k == 0:
                    kt = self.simulation.drones[u].SoC
                else:
                    sum = [(-1.0, B[f"{u},{k - 1}"])]
                    kt = 0
                sum += [(1.0, B[f"{u},{k}"]), (-CONSUMPTION_UPPER_BOUND, gamma[f"{u},{k}"])] + \
                       [(self.simulation.cost(i, j, 0), x[f"{u},{k},{i},{j}"]) for (i, j) in
                        self.simulation.edges]
                self.model.addConstr(gp.LinExpr(sum) <= kt, f"batteryconsumption1_{u},{k}")

        # eq:batteryconsumption2 = consumption if move w payload
        # B^{u,k} - B^{u,k-1} + sum_d  sum_p y^{u,k}_{d,p} * c(i,j,\omega_{d}) - M \gamma^{u,k} +M x^{u,k}_{i,j} <=  + M
        # all u, k > 1, (i,j)
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for (i, j) in self.simulation.edges:
                    sum = []
                    if k == 0:
                        kt = self.simulation.drones[u].SoC + CONSUMPTION_UPPER_BOUND
                    else:
                        sum = [(-1.0, B[f"{u},{k - 1}"])]
                        kt = CONSUMPTION_UPPER_BOUND
                    sum += [(1.0, B[f"{u},{k}"]), (-CONSUMPTION_UPPER_BOUND, gamma[f"{u},{k}"]), (CONSUMPTION_UPPER_BOUND, x[f"{u},{k},{i},{j}"])] + \
                           [(self.simulation.cost(i, j, self.simulation.deliveries[d].weight), y[f"{u},{k},{d},{p}"])
                            for d in self.simulation.deliveries.keys() for p in range(self.P)]
                    self.model.addConstr(gp.LinExpr(sum) <= kt, f"batteryconsumption2_{u},{k},{i},{j}")
        # Time
        # eq:time1 = defines the total completion time
        # C - C_{u,k} >= 0
        # all u, k
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                self.model.addConstr(CT - CU[f"{u},{k}"] >= 0, f"time1_{u},{k}")
        # eq:time2:
        # C_{u,0}=0 all u
        # eq:time3
        # C_{u,k} >= C_{u,k-1} + sum_(i,j)  x^{u,k}_{i,j} * \tau(i,j)
        # all u k
        for u in self.simulation.drones.keys():
            # k = 0
            sum = [(1.0, CU[f"{u},{0}"])] + \
                  [(-1 * self.simulation.time(i, j), x[f"{u},{0},{i},{j}"]) for (i, j) in self.simulation.edges]
            self.model.addConstr(gp.LinExpr(sum) >= 0, f"time3_{u},{0}")
            for k in range(1, self.K):
                sum = [(1.0, CU[f"{u},{k}"]), (-1.0, CU[f"{u},{k - 1}"])] + \
                      [(-self.simulation.time(i, j), x[f"{u},{k},{i},{j}"]) for (i, j) in self.simulation.edges]
                self.model.addConstr(gp.LinExpr(sum) >= 0, f"time3_{u},{k}")
        # eq:time4
        # C_{u,k} >= C_{u,k-1} + gamma_{u,k} \cdot \tau_{swap}
        # all u, k
        for u in self.simulation.drones.keys():
            # k = 0
            self.model.addConstr(CU[f"{u},{0}"] - self.simulation.swap_time * gamma[f"{u},{0}"] >= 0,
                                 f"time4_{u},{0}")
            for k in range(1, self.K):
                self.model.addConstr(
                    CU[f"{u},{k}"] - CU[f"{u},{k - 1}"] - self.simulation.swap_time * gamma[f"{u},{k}"] >= 0,
                    f"time4_{u},{k}")

        # eq:time6 link C and CD
        # C_dp >= C_uk - H ( 1 -  y_ukdp)
        # C_dp - C_uk - H y_ukdp) >= -H

        # C_uk >= C_dp - H ( 1 -  y_ukdp)
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                for u in self.simulation.drones.keys():
                    for k in range(self.K):
                        self.model.addConstr(CD[f"{d},{p}"] - CU[f"{u},{k}"] - HORIZON * y[
                            f"{u},{k},{d},{p}"] >= - HORIZON, f"time6a_{u},{k},{d},{p}")
                        self.model.addConstr(CU[f"{u},{k}"] - CD[f"{d},{p}"] - HORIZON * y[
                            f"{u},{k},{d},{p}"] >= - HORIZON, f"time6b_{u},{k},{d},{p}")

        # eq:time7 link p and p-1 completion times
        # C_dp >= C_dp-1 + sum_ij x_ukij * tau(i,j) - H (1 - y_ukdp)
        # C_dp - C_dp-1 - sum_ij x_ukij * tau(i,j) -  H y_ukdp >= - H
        for d in self.simulation.deliveries.keys():
            for p in range(1, self.P):
                for u in self.simulation.drones.keys():
                    for k in range(self.K):
                        sum = [(self.simulation.time(i, j), x[f"{u},{k},{i},{j}"]) for (i, j) in
                               self.simulation.edges]
                        self.model.addConstr(CD[f"{d},{p}"] - CD[f"{d},{p - 1}"] - HORIZON * y[
                            f"{u},{k},{d},{p}"] - gp.LinExpr(sum) >= - HORIZON,
                                             f"time7_{u},{k},{d},{p}")
        ############ Objective function ############
        #  + gp.LinExpr([(1.0, f[key]) for key in f.keys()])
        self.model.setObjective(CT, GRB.MINIMIZE)

        # self.saveMILP()

        # def saveMILP(self):
        # Save model in model.lp

        print(f"\t Saving MILP in {self.simulation.outAlgoFOLDER}/model.lp")
        self.model.write(f"{self.simulation.outAlgoFOLDER}/model.lp")

    def solveProblem(self):
        # Optimize model
        self.model.optimize()
        print(f"Gurobi status: {self.model.Status}")
        if self.model.Status == GRB.INFEASIBLE: return False
        self.exec_time = self.model.RunTime
        solution = self.extractSolution()
        return solution

    def printSolution(self):
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                print(f"{u},{k}")
                action = "idle"
                if self.model.getVarByName(f"gamma_{u},{k}").x >= 0.5:
                    print(f"gamma_{u},{k} = {self.model.getVarByName(f'gamma_{u},{k}').x}")
                    action = "swap"
                for (i, j) in self.simulation.edges:
                    if self.model.getVarByName(f"x_{u},{k},{i},{j}").x >= 0.5:
                        action = f"move from {i} to {j}"
                for d in self.simulation.deliveries.keys():
                    for p in range(self.P):
                        if self.model.getVarByName(f"y_{u},{k},{d},{p}").x >= 0.5:
                            action += f" carrying parcel {d} for its {p}th edge in path"
                print(action)

    def extractSolution(self):
        schedule = Schedule(self.simulation)
        DeliveryPaths = {}
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                tau = self.model.getVarByName(f"C_{u},{k}").x
                a = -2
                for (i,j) in self.simulation.edges:
                    if self.model.getVarByName(f'x_{u},{k},{i},{j}').x >= 0.5:
                        a = 0
                        x,y = i,j
                if self.model.getVarByName(f"gamma_{u},{k}").x >= 0.5:
                    a = -1
                    if len(schedule.plan[u])>0:
                        x = schedule.plan[u][-1].y
                    else:
                        x = self.simulation.drones[u].home.ID
                    y = x
                else:
                    for d in self.simulation.deliveries.keys():
                        for p in range(self.P):
                            if self.model.getVarByName(f'y_{u},{k},{d},{p}').x >= 0.5:
                                a = d
                                if y == self.simulation.deliveries[d].dst.ID:
                                    self.simulation.deliveries[d].arrival_time = tau

                if a > -2:
                    action = DroneAction(x, y, a, tau)
                    schedule.plan[u].append(action)
                    if a in self.simulation.deliveries.keys():
                        if a not in DeliveryPaths.keys(): DeliveryPaths[a] = []
                        DeliveryPaths[a].append(action)

        for d in self.simulation.deliveries.keys():
            for i in range(len(DeliveryPaths[d])):
                if i < len(DeliveryPaths[d])-1: DeliveryPaths[d][i].succ = DeliveryPaths[d][i+1]
                if i > 0: DeliveryPaths[d][i].pred = DeliveryPaths[d][i - 1]

        return schedule

    def getISSConstrs(self):
        for constr in self.model.getConstrs():
            if constr.getAttr('IISConstr'):
                print(f"{constr.getAttr('ConstrName')} is in ISS")

    def computeDiameter(self):
        import networkx as nx
        G = nx.Graph()
        E = [e for e in self.simulation.edges if self.simulation.cost(e[0], e[1], DRONE_MAX_PAYLOAD) < 1]
        G.add_edges_from(E)
        return nx.algorithms.diameter(G)



