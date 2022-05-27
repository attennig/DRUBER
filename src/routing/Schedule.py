from src.routing.DroneAction import *
import copy
class Schedule:
    def __init__(self, simulation, plan=None):
        self.simulation = simulation
        self.plan = plan
        if self.plan is None:
            self.plan = {u : [] for u in self.simulation.drones.keys()}

        self.arrival_times = {d: -1 for d in self.simulation.deliveries.keys()}

    def __eq__(self, other):
        return self.plan == other.plan

    def __str__(self):
        plan_str = "------------------------------"
        for u in self.plan.keys():
            plan_str += f"\n{u}:\n"
            for action in self.plan[u]:
                plan_str += f"\t{action}\n"
        return plan_str + "------------------------------\n"

    def printplan(self, plan):
        if plan is None: return
        plan_str = ""
        for u in plan:
            plan_str += f"\n{u}:\n"
            for action in plan[u]:
                plan_str += f"\t{action}\n"
        print(plan_str)

    def augment(self, u, d, idx, L, D):
        l_actions = copy.deepcopy(L)
        d_actions = copy.deepcopy(D)
        new_schedule = copy.deepcopy(self)
        i = len(new_schedule.plan[u])
        curr_soc = self.simulation.drones[u].SoC

        for action in self.plan[u]:
            if action.type == "swap": curr_soc = 1
            elif action.type == "move": curr_soc = curr_soc - action.getEnergyCost(self.simulation)

        for action in l_actions:
            if curr_soc - action.getEnergyCost(self.simulation) < 0:
                new_schedule.plan[u].append(DroneAction("swap", action.x, action.x, None, None, None))
                curr_soc = 1
            new_schedule.plan[u].append(action)
            curr_soc = curr_soc - action.getEnergyCost(self.simulation)

        for action in d_actions:

            if curr_soc - action.getEnergyCost(self.simulation) < 0:
                swap_action = DroneAction("swap", action.x, action.x, d, idx, None)
                new_schedule.plan[u].append(swap_action)
                curr_soc = 1
                idx += 1

            action.p = idx
            idx += 1
            new_schedule.plan[u].append(action)
            curr_soc = curr_soc - action.getEnergyCost(self.simulation)

        new_schedule.updateTimes(u, i)

        last_action = new_schedule.plan[u][-1]
        new_schedule.arrival_times[last_action.d] = last_action.tau


        for i in range(len(new_schedule.plan[u])):
            if new_schedule.plan[u][i].d is None: continue
            if i - 1 >= 0 and new_schedule.plan[u][i-1].p is not None:
                if new_schedule.plan[u][i].d == new_schedule.plan[u][i-1].d:
                    new_schedule.plan[u][i].pred = new_schedule.plan[u][i-1]
            if i + 1 < len(new_schedule.plan[u]) and new_schedule.plan[u][i + 1].p is not None:
                if new_schedule.plan[u][i].d == new_schedule.plan[u][i + 1].d:
                    new_schedule.plan[u][i].succ = new_schedule.plan[u][i+1]

        return new_schedule

    def updateTimes(self, u: int, i: int):
        '''
        This method updates the completion time of the actions composing the plan starting from a given action (plan[u][i])
        :param action: it is the action from which the completion time recomputation starts
        :return: void
        '''
        #print(f"updating u{u}'s plan from {i}th action")
        assert i < len(self.plan[u])
        toUpdate = [(u, i)]
        updated = []
        while len(toUpdate) > 0:

            curr_u, curr_i = toUpdate.pop(0) # pop the least recent added action
            assert curr_i < len(self.plan[curr_u])
            if updated.count((curr_u, curr_i)) > 2: #running 3:
                return False
            curr = self.plan[curr_u][curr_i]
            tau_prev = 0

            if curr_i > 0:
                prev = self.plan[curr_u][curr_i - 1]
                if prev.tau is not None: tau_prev = prev.tau
            pred = self.plan[curr_u][curr_i].pred
            tau_pred = tau_prev
            if pred is not None and pred.tau is not None:
                tau_pred = pred.tau
            curr.tau = max(tau_pred, tau_prev) + curr.getTime(self.simulation)

            updated.append((curr_u, curr_i))

            next = None
            next_t = None
            if curr_i + 1 < len(self.plan[curr_u]):
                toUpdate.append((curr_u, curr_i + 1))  # next to be updated
                next = self.plan[curr_u][curr_i + 1]
                next_t = (curr_u, curr_i + 1)
            succ = curr.succ
            succ_t = None
            if succ is not None and succ != next:
                assert succ.d == curr.d
                # need to find indices of succ
                for u_ in self.plan.keys():
                    if succ in self.plan[u_]:
                        succ_u = u_
                        succ_i = self.plan[u_].index(succ)
                        if succ_u != curr_u:
                            if succ_i < len(self.plan[succ_u]):
                                toUpdate.append((succ_u, succ_i))
                                succ_t = (succ_u, succ_i)
                        break
            #print(f"{(curr_u,curr_i)} adds {next_t} and {(succ_t)}")
        return True

    def addBatterySwaps(self, plan_keys=[]):
        if plan_keys == []: plan_keys = self.plan.keys()

        for u in plan_keys:
            SOC = self.simulation.drones[u].SoC
            i = 0

            while i < len(self.plan[u]):
                if self.plan[u][i].type != "swap":
                    consumption = self.plan[u][i].getEnergyCost(self.simulation)

                    if SOC - consumption < 0:
                        # need a battery swap before action [u][i]

                        if self.plan[u][i].d:
                            new_action = DroneAction("swap", self.plan[u][i].x, self.plan[u][i].x, self.plan[u][i].d, None, None)
                            new_action.succ = self.plan[u][i]
                            new_action.pred = self.plan[u][i].pred
                            self.plan[u][i].pred.succ = new_action
                            self.plan[u][i].pred = new_action
                            self.adjustSequenceNumbers(new_action)

                        else:
                            new_action = DroneAction("swap", self.plan[u][i].x, self.plan[u][i].x, None, None, None)
                        self.plan[u] = self.plan[u][:i] + [new_action] + self.plan[u][i:]
                        SOC = 1
                        i += 1
                    SOC -= consumption

                else:
                    # we need to check if the swap is necessary
                    # to do so we need to check if the next action is doable before the battery swap
                    if i == len(self.plan[u]) - 1:
                        self.plan[u] = self.plan[u][:i]
                    else: # if i  < len(self.plan[u]) - 1:
                        consumption = self.plan[u][i + 1].getEnergyCost(self.simulation)

                        if SOC - consumption > 0:
                            # battery does not need to be swapped
                            if i - 1 >= 0 and self.plan[u][i - 1].succ == self.plan[u][i]:
                                self.plan[u][i - 1].succ = self.plan[u][i].succ
                            if i + 1 < len(self.plan[u]) and self.plan[u][i + 1].pred == self.plan[u][i]:
                                self.plan[u][i + 1].pred = self.plan[u][i].pred
                            if self.plan[u][i].d is not None: self.adjustSequenceNumbers(self.plan[u][i])
                            self.plan[u] = self.plan[u][:i] + self.plan[u][i + 1:]

                        else:
                            SOC = 1
                            i += 1
                        SOC = SOC - consumption
                i += 1


    def getScheduleTime(self):
        CT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.tau > CT: CT = action.tau
        return CT

    def getCompletionTime(self):
        CT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                # if action.tau > CT: CT = action.tau
                if action.d in self.arrival_times.keys():
                    if action.y == self.simulation.deliveries[action.d].dst.ID:
                        self.arrival_times[action.d] = action.tau
                        if action.tau > CT: CT = action.tau
        #assert max([self.plan[u][-1].tau for u in self.plan.keys() if len(self.plan[u])>0]) == CT
        return CT

    def getMeanScheduleTime(self):
        MST = 0
        for u in self.plan.keys():
            if len(self.plan[u]) > 0:
                MST += self.plan[u][-1].tau
        return MST/len(self.plan.keys())

    def getMeanFlightTime(self):
        MFT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.type == "move":
                    MFT += action.getTime(self.simulation)
        return MFT/len(self.plan.keys())

    def getMeanSwapTime(self):
        MST = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.type == "swap":
                    MST += action.getTime(self.simulation)
        return MST/len(self.plan.keys())
    def getMeanLoadUnloadTime(self):
        MLT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.type in ["load", "unload"]:
                    MLT += action.getTime(self.simulation)
        return MLT/len(self.plan.keys())

    def getMeanWaitingTime(self):
        return self.getMeanScheduleTime() - (self.getMeanFlightTime() + self.getMeanSwapTime() + self.getMeanLoadUnloadTime())

    def getMeanDeliveryTime(self):
        MDT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                # if action.tau > CT: CT = action.tau
                if action.type == "unload" and action.d in self.arrival_times.keys():
                    if action.y == self.simulation.deliveries[action.d].dst.ID:
                        self.arrival_times[action.d] = action.tau
                        MDT += self.arrival_times[action.d]
        return MDT/len(self.arrival_times.keys())

    def getMeanScheduleDistance(self):
        MSD = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.type == "move":
                    MSD += self.simulation.dist2D(action.x, action.y)
        return MSD/len(self.plan.keys())

    def getMeanScheduleEnergy(self):
        MSE = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                w = 0
                if action.d in self.simulation.deliveries.keys(): w = self.simulation.deliveries[action.d].weight
                if action.type == "move":
                    MSE += self.simulation.cost(action.x, action.y, w)
        return MSE/len(self.plan.keys())

    def getMeanNumberSwaps(self):
        MNS = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.type == "swap":
                    MNS += 1
        return MNS / len(self.plan.keys())

    def getDroneMeanUtilizationTime(self):
        '''
        This method computes the utilization time of drones in the system.
        Computed as the time drones spend flying, swapping batteries, loading or unloading parcels / ndrones
        :return: Drone utilization time metric
        '''
        utilization_time = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                    utilization_time += action.getTime(self.simulation)
        return utilization_time / len(self.plan.keys()) #* self.getCompletionTime()

    def getDroneUtilization(self):
        '''
        This method computes the utilization of drones in the system.
        Computed as the drone mean utilization time / completion time
        :return: Drone utilization metric
        '''
        return self.getDroneMeanUtilizationTime()/self.getCompletionTime()

    def getTotalNumberParcelHandover(self):
        TPH = 0
        for d in self.simulation.deliveries.keys():
            # count how many drones carry d
            actions_dronect = []
            for u in self.simulation.drones.keys():
                for action in self.plan[u]:
                    if action.d == d:
                        actions_dronect.append((u, action.tau))
            #sort actions_dronect
            sorted_actions = sorted(actions_dronect, key=lambda tup: tup[1])
            handover_count = 0
            for i in range(len(sorted_actions)-1):
                if sorted_actions[i][0] != sorted_actions[i+1][0]:
                    # handover
                    handover_count += 1
            TPH += handover_count
        return TPH

    def getMeanNumberParceHandover(self):
        return self.getTotalNumberParcelHandover()/len(self.arrival_times.keys())

    def computeAllMetrics(self):
        self.completion_time = round(self.getCompletionTime(), 4)
        self.mean_schedule_time = round(self.getMeanScheduleTime(), 4)
        self.mean_flight_time = round(self.getMeanFlightTime(), 4)
        self.mean_swap_time = round(self.getMeanSwapTime(), 4)
        self.mean_load_unload_time = round(self.getMeanLoadUnloadTime(), 4)
        self.mean_waiting_time = round(self.getMeanWaitingTime(), 4)
        self.mean_delivery_time = round(self.getMeanDeliveryTime(), 4)
        self.mean_schedule_distance = round(self.getMeanScheduleDistance(), 4)
        self.mean_schedule_energy = round(self.getMeanScheduleEnergy(), 4)
        self.mean_number_swaps = round(self.getMeanNumberSwaps(), 4)
        self.drone_utilization_time = round(self.getDroneMeanUtilizationTime(), 4)
        self.drone_utilization = round(self.getDroneUtilization(), 4)
        self.total_number_parcel_handover = round(self.getTotalNumberParcelHandover(), 4)
        self.mean_number_parcel_handover = round(self.getMeanNumberParceHandover(), 4)

    def computeNeighbours(self, H):
        N = []
        for u1 in self.plan.keys():
            for i in range(len(self.plan[u1])):
                if self.plan[u1][i].d is None: continue
                if self.plan[u1][i].type != "move": continue
                #print(f"evaluating u{u1} {i}th action: {self.plan[u1][i]}")
                crossover_i = i
                if self.plan[u1][i-1].type == "load": crossover_i = i - 1
                if self.plan[u1][i-1].type == "swap" and i - 2 > 0 and self.plan[u1][i-2].type == "load": crossover_i = i - 2

                HS = self.plan[u1][crossover_i].x
                #print(f"crossover action {self.plan[u1][crossover_i]}")

                #print(self)
                for u2 in self.plan.keys():
                    if u1 == u2: continue
                    #print(f"u{u2}")
                    if len(self.plan[u2]) == 0:
                        #print(f"- no action")
                        CS = self.simulation.drones[u2].home.ID
                        if CS != HS and self.simulation.cost(CS, HS, 0) > 1: continue

                        new_plan = copy.deepcopy(self.plan)
                        #self.printplan(new_plan)
                        part1_u1 = copy.copy(new_plan[u1][:crossover_i])
                        part2_u1 = copy.copy(new_plan[u1][crossover_i:])
                        #print(f"part1_u1: {[f'{action}' for action in part1_u1]}\npart2_u1: {[f'{action}' for action in part2_u1]}")
                        HA = part2_u1[0]
                        #print(f"handover action {HA}")
                        part1_u2 = []  # copy.copy(new_plan[u2][:j])
                        part2_u2 = []  # copy.copy(new_plan[u2][j:])
                        part_add_u1 = []
                        part_add_u2 = []

                        if CS != HS:
                            assert self.simulation.cost(CS, HS, 0) <= 1
                            movement_action = DroneAction("move", CS, HS, None, None, None)
                            part1_u2 = [movement_action]

                        if HA.type == "move":
                            load_action = DroneAction("load", HS, HS, HA.d, None, None)
                            part_add_u2 += [load_action]

                            unload_action = DroneAction("unload", HS, HS, HA.d, None, None)
                            part_add_u1 += [unload_action]
                            assert HA.pred.type != "load"

                            part1_u1[-1].succ = unload_action
                            unload_action.pred = part1_u1[-1]
                            unload_action.succ = load_action
                            load_action.pred = unload_action
                            load_action.succ = HA
                            HA.pred = load_action

                        new_plan[u1] = part1_u1 + part_add_u1 + part2_u2
                        new_plan[u2] = part1_u2 + part_add_u2 + part2_u1

                        new_schedule = Schedule(self.simulation, new_plan)

                        new_schedule.addBatterySwaps([u1, u2])
                        new_schedule.adjustSequenceNumbers(HA)
                        feasible = True
                        if len(new_schedule.plan[u1]) > 0: feasible = new_schedule.updateTimes(u1, 0)
                        if len(new_schedule.plan[u2]) > 0: feasible = feasible and new_schedule.updateTimes(u2, 0)
                        if feasible and new_schedule.getScheduleTime() < H:
                            new_schedule.check()
                            N.append(new_schedule)

                    else:
                        for j in range(len(self.plan[u2])):
                            #print(f"- action{j}")
                            if self.plan[u1][i].d == self.plan[u2][j].d: continue
                            if self.plan[u2][j].type != "move": continue
                            #print(f"evaluating u{u2} {j}th action: {self.plan[u2][j]}")

                            if self.plan[u2][j].d:
                                w = self.simulation.deliveries[self.plan[u2][j].d].weight
                            else:
                                w = 0

                            CS = self.plan[u2][j].x
                            AS = self.plan[u2][j].y

                            if CS != HS and (AS == HS or self.simulation.cost(CS, HS, w) > 1 or self.simulation.cost(HS, AS,w) > 1): continue

                            new_plan = copy.deepcopy(self.plan)
                            if CS != HS:
                                #print("starting plan")
                                #self.printplan(new_plan)
                                assert self.simulation.cost(CS, HS, w) <= 1
                                movement_action1 = DroneAction("move", CS, HS, new_plan[u2][j].d, None, None)
                                movement_action2 = DroneAction("move", HS, AS, new_plan[u2][j].d, None, None)
                                if self.plan[u2][j].d:
                                    if new_plan[u2][j].pred: new_plan[u2][j].pred.succ = movement_action1
                                    movement_action1.pred = new_plan[u2][j].pred
                                    movement_action1.succ = movement_action2
                                    movement_action2.pred = movement_action1
                                    movement_action2.succ = new_plan[u2][j].succ
                                    if new_plan[u2][j].succ: new_plan[u2][j].succ.pred = movement_action2

                                new_plan[u2] = new_plan[u2][:j] + [movement_action1, movement_action2] + new_plan[u2][j+1:]
                                crossover_j = j+1
                                #print("modified plan")
                                #self.printplan(new_plan)

                            else:
                                crossover_j = j
                                if new_plan[u2][crossover_j - 1].type == "load": crossover_j = j - 1
                                if new_plan[u2][j - 1].type == "swap" and j - 2 > 0 and new_plan[u2][j - 2].type == "load": crossover_j = j - 2
                            #print(f"crossover action: {new_plan[u2][crossover_j]}")

                            #self.printplan(new_plan)

                            part1_u1 = copy.copy(new_plan[u1][:crossover_i])
                            part2_u1 = copy.copy(new_plan[u1][crossover_i:])
                            HA_from_u1 = part2_u1[0]
                            assert HA_from_u1.type in ["load", "move"]
                            
                            part1_u2 = copy.copy(new_plan[u2][:crossover_j])
                            part2_u2 = copy.copy(new_plan[u2][crossover_j:])
                            HA_from_u2 = part2_u2[0]
                            assert HA_from_u2.type in ["load", "move"]

                            assert HA_from_u2.x == HS
                            assert HA_from_u1.x == HS

                            part_add_u1 = []
                            part_add_u2 = []


                            # define part_add_u* adding load, unload actions
                            if HA_from_u1.type == "move":
                                # need to add load and unload for the parcel carried by u1
                                unload_u1 = DroneAction("unload", HS, HS, HA_from_u1.d, None, None)
                                part_add_u1 = [unload_u1]

                                assert HA_from_u1.pred.type != "load"

                                load_u2 = DroneAction("load", HS, HS, HA_from_u1.d, None, None)
                                part_add_u2 = [load_u2]

                                HA_from_u1.pred.succ = unload_u1
                                unload_u1.pred = HA_from_u1.pred
                                unload_u1.succ = load_u2
                                load_u2.pred = unload_u1
                                load_u2.succ = HA_from_u1
                                HA_from_u1.pred = load_u2



                            if HA_from_u2.d and HA_from_u2.type == "move":
                                # need to add load and unload for the parcel carried by u2
                                unload_u2 = DroneAction("unload", HS, HS, HA_from_u2.d, None, None)
                                part_add_u2 = [unload_u2] + part_add_u2

                                load_u1 = DroneAction("load", HS, HS, HA_from_u2.d, None, None)
                                part_add_u1 = part_add_u1 + [load_u1]

                                HA_from_u2.pred.succ = unload_u2
                                unload_u2.pred = HA_from_u2.pred

                                unload_u2.succ = load_u1
                                load_u1.pred = unload_u2
                                load_u1.succ = HA_from_u2
                                HA_from_u2.pred = load_u1

                            else:
                                assert HA_from_u2.type == "load" or HA_from_u2.d is None
                                # no need to add load and unload of the parcel carried by u2

                            # if self.containSuccessors(part1_u1, part_add_u1 + part2_u2): continue
                            # if self.containSuccessors(part1_u2, part_add_u2 + part2_u1): continue
                            # if self.containSuccessors(part1_u1, part_add_u2 + part2_u1): continue
                            # if self.containSuccessors(part1_u2, part_add_u1 + part2_u2): continue
                            new_plan[u1] = part1_u1 + part_add_u1 + part2_u2
                            new_plan[u2] = part1_u2 + part_add_u2 + part2_u1

                            new_schedule = Schedule(self.simulation, new_plan)

                            new_schedule.addBatterySwaps([u1, u2])
                            new_schedule.adjustSequenceNumbers(HA_from_u1)
                            if HA_from_u2.d is not None: new_schedule.adjustSequenceNumbers(HA_from_u2)
                            feasible = True
                            if len(new_schedule.plan[u1]) > 0: feasible = new_schedule.updateTimes(u1, 0)
                            if len(new_schedule.plan[u2]) > 0: feasible = feasible and new_schedule.updateTimes(u2, 0)
                            if feasible and new_schedule.getScheduleTime() < H:
                                new_schedule.check()
                                #print(f"{self} generates :{new_schedule}")
                                N.append(new_schedule)

        #print(N)
        return N


    def adjustSequenceNumbers(self, action):
        curr_action = action
        while curr_action.pred is not None:
            curr_action = curr_action.pred
            assert curr_action.d == action.d

        idx = 0
        while curr_action.succ is not None:
            curr_action.p = idx
            idx += 1
            curr_action = curr_action.succ
            assert curr_action.d == action.d
        curr_action.p = idx

    def containSuccessors(self, part1, part2):
        for action in part2:
            while action.succ is not None:
                action = action.succ
                if action in part1: return True
        return False


    def check(self):
        for d in self.simulation.deliveries.keys():
            for u in self.plan.keys():
                pos = []
                for i in range(len(self.plan[u])):
                    if self.plan[u][i].d is not None and self.plan[u][i].d == d:
                        assert self.plan[u][i].p is not None
                        pos.append(self.plan[u][i].p)
                for j in range(len(pos)-1):
                    if pos[j] >= pos[j+1]:

                        print(self)
                        assert pos[j] < pos[j+1]



