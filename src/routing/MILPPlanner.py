import gurobipy as gp
from gurobipy import GRB
import os
from src.routing.PathPlanner import *


class MILPPlanner(PathPlanner):
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
        '''
        This method define the problem setting up variables, constraints and optimization function.
        VARS:
            -BINARY: delta{u,k}_{t} = 1 if u's k-th action is of type t;0 otw. for u,k, t in[move, swap, load, unload, idle]
            -BINARY: x^{u,k}_{s} = 1 if the departing station is s in S;0 otw.
            -BINARY: y^{u,k}_{s} = 1 if the arrival station is s in S;0 otw.
            -BINARY: seq^{u,k}_{d,p} = 1 if p is the sequence number of action u k which involves d;0 otw.
            -BINARY: delivered_{d,u,k,p} = 1 if parcel d is unloded at destination by u in its k-th activity;0 otw.
            -CONTINUOUS: B^{u,k} = u's battery State of Charge at the end of k-th activity.
            -CONTINUOUS: C^{u,k} = completion time of job scheduled as u's k-th activity.
            -CONTINUOUS: CT = completion time
        :return: void
        '''
        print(f"\t Setting up MILP")

        diameter = self.computeDiameter()
        self.K = 3 * diameter # actions
        self.P = 3 * diameter # involvements
        print(f"{self.K}, {self.P}")
        TYPES = ["move", "swap", "load", "unload", "idle"]

        '''
        delta[f"{u},{k},{t}"]
        x[f"{u},{k},{s}"]
        y[f"{u},{k},{s}"]
        seq[f"{u},{k},{d},{p}"]
        delivered[f"{d},{u},{k},{p}"]
        B[f"{u},{k}"]
        C[f"{u},{k}"]
        CT
        '''

        ############ Variables #############
        # BINARY: delta{u,k}_{t} = 1 if u's k-th action is of type t;0 otw.
        # for u, k, t in [move, swap, load, unload, idle]
        delta = {}  # delta[f"{u},{k},{t}"], f"delta_{u},{k},{t}"
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for t in TYPES:
                    delta[f"{u},{k},{t}"] = self.model.addVar(vtype=GRB.BINARY, name=f"delta_{u},{k},{t}")

        # BINARY: x^{u,k}_{s} = 1 if the departing station is s in S;0 otw.
        # BINARY: y^{u,k}_{s} = 1 if the arrival station is s in S;0 otw.
        x = {}  # x[f"{u},{k},{s}"], f"x_{u},{k},{s}"
        y = {}  # y[f"{u},{k},{s}"], f"y_{u},{k},{s}"
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for s in self.simulation.stations.keys():
                    x[f"{u},{k},{s}"] = self.model.addVar(vtype=GRB.BINARY, name=f"x_{u},{k},{s}")
                    y[f"{u},{k},{s}"] = self.model.addVar(vtype=GRB.BINARY, name=f"y_{u},{k},{s}")

        # BINARY: seq^{u,k}_{d,p} = 1 if p is the sequence number of action u k which involves d;0 otw.
        # all d, p, u, k
        seq = {} # seq[f"{u},{k},{d},{p}"], f"seq_{u},{k},{d},{p}"
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                for u in self.simulation.drones.keys():
                    for k in range(self.K):
                        seq[f"{u},{k},{d},{p}"] = self.model.addVar(vtype=GRB.BINARY, name=f"seq_{u},{k},{d},{p}")

        # BINARY: delivered_{d,u,k} = 1 if parcel d is unloded at destination by u in its k-th activity;0 otw. for d
        # all d, u ,k
        delivered = {}  # delivered[f"{u},{k},{d},{p}"], f"delivered_{u},{k},{d},{p}"

        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for d in self.simulation.deliveries.keys():
                    delivered[f"{u},{k},{d}"] = self.model.addVar(vtype=GRB.BINARY,
                                                                      name=f"delivered_{u},{k},{d}")

                    #for p in range(self.P):
                        #delivered[f"{u},{k},{d},{p}"] = self.model.addVar(vtype=GRB.BINARY, name=f"delivered_{u},{k},{d},{p}")

        # CONTINUOUS : B^{u,k} = u's battery State of Charge at the end of $k$-th activity.
        # all u, k
        B = {} # f"B_{u},{k}"
        for u in self.simulation.drones.keys():
            for k in range(-1,self.K):
                B[f"{u},{k}"] = self.model.addVar(vtype=GRB.CONTINUOUS, name=f"B_{u},{k}", lb=0, ub=1)

        # CONTINUOUS : C^{u,k} = completion time of job scheduled as u's k-th activity.
        # all u, k
        C = {} # f"C_{u},{k}"
        for u in self.simulation.drones.keys():
            for k in range(-1,self.K):
                C[f"{u},{k}"] = self.model.addVar(vtype=GRB.CONTINUOUS, name=f"C_{u},{k}")

        # CONTINUOUS : C = completion time
        CT = self.model.addVar(vtype=GRB.CONTINUOUS, name="C")




        ############ Constraints #############

        # Actions


        # Each action must have exactly one type, one s_loc, one e_loc
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                # sum_{t in Types} delta{u,k}_{t} = 1
                self.model.addConstr(
                    gp.LinExpr([(1.0, delta[f"{u},{k},{t}"]) for t in TYPES]) == 1,
                    f"oneType_{u},{k}")
                # sum_{s in S} x^{u,k}_{s} = 1
                self.model.addConstr(
                    gp.LinExpr([(1.0, x[f"{u},{k},{s}"]) for s in self.simulation.stations.keys()]) == 1,
                    f"oneSLoc_{u},{k}")
                # sum_{s in S} y^{u,k}_{s} = 1
                self.model.addConstr(
                    gp.LinExpr([(1.0, y[f"{u},{k},{s}"]) for s in self.simulation.stations.keys()]) == 1,
                    f"oneELoc_{u},{k}")

        # Each action can involve at most one parcel
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                # sum_{d in D} sum_{p} seq^{u,k}_{d,p} <= 1
                self.model.addConstr(
                    gp.LinExpr([(1.0, seq[f"{u},{k},{d},{p}"]) for d in self.simulation.deliveries.keys() for p in range(self.P)]) <= 1,
                    f"eachActionOneParcel_{u},{k}")

        # Each parcel is involved in at most one action at time
        for d in self.simulation.deliveries.keys():
            for p in range(self.P):
                # sum_{u} sum_{k} seq^{u,k}_{d,p} <= 1
                self.model.addConstr(
                    gp.LinExpr([(1.0, seq[f"{u},{k},{d},{p}"]) for u in self.simulation.drones.keys() for k in range(self.K)]) <= 1,
                    f"eachParcelOneAction_{d},{p}")

        # not move does not change station, move does change station
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for s in self.simulation.stations.keys():
                    # x^{u,k}_{s} + (1-delta{u,k}_{t}) - y^{u,k}_{s} <= 1
                    self.model.addConstr(
                         x[f"{u},{k},{s}"] + (1-delta[f"{u},{k},move"])  - y[f"{u},{k},{s}"] <= 1,
                        f"notMove_{u},{k},{s}")

                    # x^{u,k}_{s} + y^{u,k}_{s} + delta{u,k}_{move}  <= 2
                    self.model.addConstr(
                        x[f"{u},{k},{s}"] + y[f"{u},{k},{s}"] + delta[f"{u},{k},move"] <= 2,
                        f"move_{u},{k},{s}")

        #   If a parcel is loaded/unloaded then it is assigned consistently
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                # delta^{u,k}_{(un)load} - sum_{d,p} seq^{u,k}_{d,p} <= 0
                self.model.addConstr(
                    delta[f"{u},{k},load"]
                    - gp.LinExpr([(1.0, seq[f"{u},{k},{d},{p}"]) for d in self.simulation.deliveries.keys() for p in range(self.P) ])
                    <= 0,
                    f"loadAssignment_{u},{k}")
                self.model.addConstr(
                    delta[f"{u},{k},unload"]
                    - gp.LinExpr([(1.0, seq[f"{u},{k},{d},{p}"]) for d in self.simulation.deliveries.keys() for p in range(self.P)])
                    <= 0,
                    f"unloadAssignment_{u},{k}")



        # Drones’ flows

        # 	Each drone starts from its initial location
        for u in self.simulation.drones.keys():
            #x^{u,1}_{sigma_{u}} = 1
            self.model.addConstr(x[f"{u},{0},{self.simulation.drones[u].home.ID}"] == 1, f"home_{u}")
        # 	Each drone departs from the station in which it was located after executing the previous action
        for u in self.simulation.drones.keys():
            for k in range(1,self.K):
                for s in self.simulation.stations.keys():
                    # x^{u,k}_{s} = y^{u,k-1}_{s}
                    self.model.addConstr(x[f"{u},{k},{s}"] == y[f"{u},{k-1},{s}"], f"movementConsistency_{u},{k},{s}")

        # Deliveries’ flows

        # 	Each parcel is delivered exactly once
        for d in self.simulation.deliveries.keys():
            # sum_{u,k} delivered_{d,u,k} = 1
            '''self.model.addConstr(
                gp.LinExpr(
                    [(1.0, delivered[f"{u},{k},{d},{p}"])
                     for u in self.simulation.drones.keys()
                     for k in range(self.K) for p in range(self.P)] ) == 1,
                f"eachParcelDeliveredOnce_{d}")'''
            self.model.addConstr(
                gp.LinExpr(
                    [(1.0, delivered[f"{u},{k},{d}"])
                     for u in self.simulation.drones.keys()
                     for k in range(self.K)]) == 1,
                f"eachParcelDeliveredOnce_{d}")

        # 	Delivery accomplishment definition
        for d in self.simulation.deliveries.keys():
            dst_d = self.simulation.deliveries[d].dst.ID
            for u in self.simulation.drones.keys():
                for k in range(self.K):
                    # sum_{p} seq^{u,k}_{d,p} + y^{u,k}_{dst_d} + delta^{u,k}_{unload}  - delivered^{u,k}_{d}<= 2
                    self.model.addConstr(
                        gp.LinExpr([(1.0,seq[f"{u},{k},{d},{p}"]) for p in range(self.P)])
                        + y[f"{u},{k},{dst_d}"] + delta[f"{u},{k},unload"]
                        - delivered[f"{u},{k},{d}"] <= 2,
                        f"deliveryDef<_{d},{u},{k}")
                    # 3* delivered^{u,k}_{d} - (y^{u,k}_{dst_d} + delta^{u,k}_{unload} + sum_{p} seq^{u,k}_{d,p}) <= 0
                    self.model.addConstr(
                        3 * delivered[f"{u},{k},{d}"]
                        - (gp.LinExpr([(1.0,seq[f"{u},{k},{d},{p}"]) for p in range(self.P)])  + y[f"{u},{k},{dst_d}"] + delta[f"{u},{k},unload"]) <= 0,
                        f"deliveryDef>_{d},{u},{k}")
                    '''for p in range(self.P):
                        # seq^{u,k}_{d,p} + y^{u,k}_{dst_d} + delta{u,k}_{unload} - delivered_{d,u,k,p} <= 2
                        self.model.addConstr(
                            seq[f"{u},{k},{d},{p}"] + y[f"{u},{k},{dst_d}"] + delta[f"{u},{k},unload"]
                            - delivered[f"{u},{k},{d},{p}"] <= 2,
                            f"deliveryDef<_{d},{u},{k},{p}")
                        self.model.addConstr(
                            3 * delivered[f"{u},{k},{d},{p}"]
                            - (seq[f"{u},{k},{d},{p}"] + y[f"{u},{k},{dst_d}"] + delta[f"{u},{k},unload"]) <= 0,
                            f"deliveryDef>_{d},{u},{k},{p}")'''

        # 	Each parcel is first loaded in its source station
        for d in self.simulation.deliveries.keys():
            self.model.addConstr(
                gp.LinExpr([(1.0, seq[f"{u},{k},{d},{0}"]) for u in self.simulation.drones.keys() for k in range(self.K)]) == 1,
                f"firstLoad_{d}")
            for u in self.simulation.drones.keys():
                for k in range(self.K):
                    # 2*seq^{u,k}_{d,1} <=  delta{u,k}_{load} + x^{u,k}_{src_d}
                    src_d = self.simulation.deliveries[d].src.ID
                    self.model.addConstr(
                        2*seq[f"{u},{k},{d},{0}"] - delta[f"{u},{k},load"] - x[f"{u},{k},{src_d}"] <= 0,
                        f"firstLoad_{d},{u},{k}")


        # 	For each drone action involving a parcel, such parcel it is either unloaded or also the next action involves it.
        for d in self.simulation.deliveries.keys():
            for u in self.simulation.drones.keys():
                for k in range(self.K):
                    for p in range(self.P):
                        if k == 0 or p == 0:
                            self.model.addConstr(
                                seq[f"{u},{k},{d},{p}"] <= delta[f"{u},{k},load"],
                                f"prevAction_{u},{k},{d},{p}"
                            )
                        else:
                            self.model.addConstr(
                                seq[f"{u},{k},{d},{p}"] <= delta[f"{u},{k},load"] + seq[f"{u},{k-1},{d},{p-1}"],
                                f"prevAction_{u},{k},{d},{p}"
                            )
                        if k == self.K - 1 or p == self.P - 1:
                            self.model.addConstr(
                                seq[f"{u},{k},{d},{p}"] <= delta[f"{u},{k},unload"],
                                f"nextAction_{u},{k},{d},{p}"
                            )
                        else:
                            self.model.addConstr(
                                seq[f"{u},{k},{d},{p}"] <= delta[f"{u},{k},unload"] + seq[f"{u},{k+1},{d},{p+1}"],
                                f"nextAction_{u},{k},{d},{p}"
                            )





        for d in self.simulation.deliveries.keys():
            for p in range(self.P-1):
                for u1 in self.simulation.drones.keys():
                    for k1 in range(self.K):
                        for u2 in self.simulation.drones.keys():
                            for k2 in range(self.K):
                                for s in self.simulation.stations.keys():
                                    self.model.addConstr(
                                        seq[f"{u1},{k1},{d},{p}"] + y[f"{u1},{k1},{s}"] + seq[f"{u2},{k2},{d},{p+1}"] - x[f"{u2},{k2},{s}"] <= 2,
                                        f"{d},{p},{u1},{k1},{u2},{k2},{s}")
                                    self.model.addConstr(
                                        seq[f"{u1},{k1},{d},{p}"] - y[f"{u1},{k1},{s}"] + seq[f"{u2},{k2},{d},{p + 1}"] + x[f"{u2},{k2},{s}"] <= 2,
                                        f"bis{d},{p},{u1},{k1},{u2},{k2},{s}")

        for d in self.simulation.deliveries.keys():
            for p in range(1,self.P):
                self.model.addConstr(
                    gp.LinExpr([(1.0, seq[f"{u},{k},{d},{p}"]) for u in self.simulation.drones.keys() for k in range(self.K)]) <=
                    gp.LinExpr([(1.0, seq[f"{u},{k},{d},{p-1}"]) for u in self.simulation.drones.keys() for k in range(self.K)]),
                    f"nogaps_{d},{p}")

        '''
                delta[f"{u},{k},{t}"]
                x[f"{u},{k},{s}"]
                y[f"{u},{k},{s}"]
                seq[f"{u},{k},{d},{p}"]
                delivered[f"{d},{u},{k},{p}"]
                B[f"{u},{k}"]
                C[f"{u},{k}"]
                CT
                '''



        # Time

        #   init
        for u in self.simulation.drones.keys():
            self.model.addConstr(C[f"{u},{-1}"] == 0, f"socInit_{u}")
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                # C^{u,k} >= C^{u,k-1} + delta{u,k}_{load} \Delta_{t}^{load}
                self.model.addConstr(C[f"{u},{k}"] - C[f"{u},{k-1}"] - self.simulation.load_time * delta[f"{u},{k},load"] >= 0,
                                     f"loadTime_{u},{k}")
                # C^{u,k} >= C^{u,k-1} + delta{u,k}_{unload} \Delta_{t}^{unload}

                self.model.addConstr(C[f"{u},{k}"] - C[f"{u},{k-1}"] - self.simulation.unload_time * delta[f"{u},{k},unload"] >= 0,
                                     f"unloadTime_{u},{k}")

                # C^{u,k} >= C^{u,k-1} + delta{u,k}_{swap} \Delta_{t}^{swap}
                self.model.addConstr(C[f"{u},{k}"] - C[f"{u},{k-1}"] - self.simulation.swap_time * delta[f"{u},{k},swap"] >= 0,
                                     f"swapTime_{u},{k}")

                # C^{u,k} >= C^{u,k-1} + delta{u,k}_{move} \Delta_{t}^{move}(i,j) - H (2 - (x^{u,k}_{i} + y^{u,k}_{j}))
                # - H2 + Hx^{u,k}_{i} + Hy^{u,k}_{j}
                # all (i,j) in E
                for (i, j) in self.simulation.edges:
                    self.model.addConstr(C[f"{u},{k}"] >=  C[f"{u},{k-1}"] + self.simulation.time(i, j)
                                         - self.simulation.horizon *(3 - (delta[f"{u},{k},move"] + x[f"{u},{k},{i}"] + y[f"{u},{k},{j}"])),
                                         f"moveTime_{u},{k},{i},{j}")

        for d in self.simulation.deliveries.keys():
            for p in range(1,self.P):
                for u in self.simulation.drones.keys():
                    for k in range(self.K):
                        for u2 in self.simulation.drones.keys():
                            for k2 in range(self.K):
                                self.model.addConstr(
                                    C[f"{u},{k}"] >=
                                    C[f"{u2},{k2}"] + self.simulation.load_time * delta[f"{u},{k},load"]
                                    + self.simulation.unload_time * delta[f"{u},{k},unload"] + self.simulation.swap_time * delta[f"{u},{k},swap"]
                                    - self.simulation.horizon * (2 - (seq[f"{u},{k},{d},{p}"] + seq[f"{u2},{k2},{d},{p - 1}"])),
                                    f"deliveryPred_{d},{p},{u},{k},{u2},{k2}")
                                for (i, j) in self.simulation.edges:
                                    self.model.addConstr(
                                        C[f"{u},{k}"] >=
                                        C[f"{u2},{k2}"] + self.simulation.time(i, j)
                                        - self.simulation.horizon * (5 - (delta[f"{u},{k},move"] + x[f"{u},{k},{i}"] + y[f"{u},{k},{j}"] + seq[f"{u},{k},{d},{p}"] + seq[f"{u2},{k2},{d},{p - 1}"])),
                                        f"deliveryPred_{d},{p},{u},{k},{u2},{k2},{i},{j}")
                                '''# C^{u,k} >= C^{u2,k2} - H (2-(seq^{u,k}_{d,p} + seq^{u2,k2}_{d,p-1}))
                                # C^{u,k} >= C^{u2,k2} - H (2-seq^{u,k}_{d,p} - seq^{u2,k2}_{d,p-1}))
                                # -2H + H*seq^{u,k}_{d,p} + H*seq^{u2,k2}_{d,p-1}
                                
                                self.model.addConstr(
                                    C[f"{u},{k}"] - C[f"{u2},{k2}"] - self.simulation.horizon * seq[f"{u},{k},{d},{p}"]
                                    - self.simulation.horizon * seq[f"{u2},{k2},{d},{p-1}"] >= -2 * self.simulation.horizon,
                                    f"deliveryPred_{d},{p},{u},{k},{u2},{k2}")'''

        # CT >= C^{u,k}
        # Completion time
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                self.model.addConstr(CT - C[f"{u},{k}"] >= 0, f"completionTimeDef_{u},{k}")


        # Battery

        # 	Battery swap

        #   init
        for u in self.simulation.drones.keys():
            self.model.addConstr(B[f"{u},{-1}"] == self.simulation.drones[u].SoC, f"socInit_{u}")

        # 	swap
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                # B^{u,k} >= delta_{u,k}_{swap}
                self.model.addConstr(B[f"{u},{k}"] - delta[f"{u},{k},swap"] >= 0, f"batterySwap_{u},{k}")

        #   Consumption load, unload, idle
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                # B^{u,k-1} <=  B^{u,k-1} + M (1-(delta{u,k}_{load} + delta{u,k}_{unload} + delta{u,k}_{idle}))
                self.model.addConstr(
                    B[f"{u},{k}"] <= B[f"{u},{k-1}"] +
                    CONSUMPTION_UPPER_BOUND * (1 - (delta[f"{u},{k},load"] + delta[f"{u},{k},unload"] + delta[f"{u},{k},idle"]) ),
                    f"noConsumption_{u},{k}")

        # 	Consumption in case no parcel is involved
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for i in self.simulation.stations.keys():
                    for j in self.simulation.stations.keys():
                        if i == j: continue
                        self.model.addConstr(B[f"{u},{k}"] <=  B[f"{u},{k-1}"] - self.simulation.cost(i,j,0)
                                             + CONSUMPTION_UPPER_BOUND * (4 - (
                                                        x[f"{u},{k},{i}"] + y[f"{u},{k},{j}"] + delta[f"{u},{k},move"]
                                                        + (1 - gp.LinExpr([(1.0,seq[f"{u},{k},{d},{p}"]) for d in self.simulation.deliveries.keys() for p in range(self.P)]))
                                                        )), f"batteryConsumptionNoPayload_{u},{k},{i},{j}")

        # 	Consumption in case a parcel is involved
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                for i in self.simulation.stations.keys():
                    for j in self.simulation.stations.keys():
                        if i == j: continue
                        for d in self.simulation.deliveries.keys():
                            w_d = self.simulation.deliveries[d].weight
                            self.model.addConstr(B[f"{u},{k}"] <= B[f"{u},{k-1}"] - self.simulation.cost(i,j,w_d)
                                                + CONSUMPTION_UPPER_BOUND * (4 - (
                                                        x[f"{u},{k},{i}"] + y[f"{u},{k},{j}"] + delta[f"{u},{k},move"]
                                                        + gp.LinExpr([(1.0,seq[f"{u},{k},{d},{p}"]) for p in range(self.P)])
                                                        )), f"batteryConsumptionWPayload_{u},{k},{i},{j}")

        ############ Objective function ############
        #  + gp.LinExpr([(1.0, f[key]) for key in f.keys()])
        # + gp.LinExpr([(1.0,C[f"{u},{k}"]) for u in self.simulation.drones.keys() for k in range(self.K)])
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

        #if self.model.Status == GRB.INFEASIBLE:
        #    self.getISSConstrs()
        #    return None
        #self.exec_time = self.model.RunTime
        solution = self.extractSolution()

        #self.printSolution()
        return solution

    def printVars(self):
        for var in self.model.getVars():
            print(f"{var.VarName} = {var.x}")

    def extractSolution(self):
        #self.printVars()
        schedule = Schedule(self.simulation)
        DeliveryPaths = { d : [] for d in self.simulation.deliveries.keys()}
        for u in self.simulation.drones.keys():
            for k in range(self.K):
                if self.model.getVarByName(f"delta_{u},{k},move").x >= 0.5: t = "move"
                if self.model.getVarByName(f"delta_{u},{k},load").x >= 0.5: t = "load"
                if self.model.getVarByName(f"delta_{u},{k},unload").x >= 0.5: t = "unload"
                if self.model.getVarByName(f"delta_{u},{k},swap").x >= 0.5: t = "swap"
                if self.model.getVarByName(f"delta_{u},{k},idle").x >= 0.5: t = "idle"
                for s in self.simulation.stations.keys():
                    if self.model.getVarByName(f"x_{u},{k},{s}").x >= 0.5: x = s
                    if self.model.getVarByName(f"y_{u},{k},{s}").x >= 0.5: y = s
                delivery = None
                seq = None
                for d in self.simulation.deliveries.keys():
                    for p in range(self.P):
                        if self.model.getVarByName(f"seq_{u},{k},{d},{p}").x >= 0.5:
                            delivery = d
                            seq = p


                tau = self.model.getVarByName(f"C_{u},{k}").x

                action = DroneAction(t, x, y, delivery, seq, tau)

                #if len(schedule.plan[u]) > 0:
                    #action.prev = schedule.plan[u][-1]
                    #schedule.plan[u][-1].next = action
                schedule.plan[u].append(action)

                if delivery in self.simulation.deliveries.keys():
                    DeliveryPaths[delivery].append(action)

            for d in self.simulation.deliveries.keys():
                for i in range(len(DeliveryPaths[d])):
                    if i < len(DeliveryPaths[d]) - 1: DeliveryPaths[d][i].succ = DeliveryPaths[d][i + 1]
                    if i > 0: DeliveryPaths[d][i].pred = DeliveryPaths[d][i - 1]
        print(schedule)
        return schedule

    def getISSConstrs(self):
        self.model.computeIIS()
        self.model.write("model.ilp")
        for constr in self.model.getConstrs():
            if constr.getAttr('IISConstr'):
                print(f"{constr.getAttr('ConstrName')} is in ISS")

    def computeDiameter(self):
        import networkx as nx
        G = nx.Graph()
        E = [e for e in self.simulation.edges if self.simulation.cost(e[0], e[1], DRONE_MAX_PAYLOAD) < 1]
        G.add_edges_from(E)
        return nx.algorithms.diameter(G)