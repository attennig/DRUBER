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
        plan_str = ""
        for u in self.plan.keys():
            plan_str += f"\n{u}:\n"
            for action in self.plan[u]:
                plan_str += f"\t{action}\n"
        return plan_str

    def printplan(self, plan):
        if plan is None: return
        plan_str = ""
        for u in plan:
            plan_str += f"\n{u}:\n"
            for action in plan[u]:
                plan_str += f"\t{action}\n"
        print(plan_str)

    def isValid(self):
        #print(self)
        for u in self.plan.keys():
            assert u in self.simulation.drones.keys()
            #if len(self.plan[u]) > 0: assert self.plan[u][-1].a != 0
            for i in range(len(self.plan[u])):
                #print(f"ACTOIN x{action.x}, y{action.y}")
                assert self.plan[u][i].a in [-1,0] or self.plan[u][i].a in self.simulation.deliveries.keys()
                assert self.plan[u][i].x in self.simulation.stations.keys()
                assert self.plan[u][i].y in self.simulation.stations.keys()
                if i > 0: assert self.plan[u][i].tau >= self.plan[u][i-1].tau
                if self.plan[u][i].pred is not None: assert self.plan[u][i].a == self.plan[u][i].pred.a
                if self.plan[u][i].succ is not None: assert self.plan[u][i].a == self.plan[u][i].succ.a

    def updateTimes(self, u, i):
        if i >= len(self.plan[u]): return True
        toUpdate = [(u,i)]
        updated = []
        while len(toUpdate) > 0:

            curr_u, curr_i = toUpdate.pop(0)
            assert curr_i < len(self.plan[curr_u])

            if (curr_u, curr_i) in updated:
                #print("This schedule has loop")
                return False

            curr = self.plan[curr_u][curr_i]

            tau_prev = 0
            if curr_i > 0:
                prev = self.plan[curr_u][curr_i - 1]
                tau_prev = prev.tau
            pred = self.plan[curr_u][curr_i].pred
            tau_pred = tau_prev
            if pred is not None:
                assert pred.a == curr.a
                tau_pred = pred.tau
            curr.tau = max(tau_pred, tau_prev) + curr.getTime(self.simulation)
            updated.append((curr_u, curr_i))

            next = None
            if curr_i + 1 < len(self.plan[curr_u]):
                toUpdate.append((curr_u, curr_i+1)) # next to be updated
                next = self.plan[curr_u][curr_i+1]
            succ = curr.succ
            if succ is not None and succ != next:
                assert succ.a == curr.a
                # need to find indices of succ
                for u_ in self.plan.keys():
                    if succ in self.plan[u_]:
                        succ_u = u_
                        succ_i = self.plan[u_].index(succ)
                        if succ_u != curr_u:
                            if succ_i < len(self.plan[succ_u]):
                                toUpdate.append((succ_u, succ_i))
                        break
        return True

        '''
        if i >= len(self.plan[u]):
            print("caso baso returning")
            return
        curr = self.plan[u][i]

        tau_prev = 0
        if i > 0:
            prev = self.plan[u][i - 1]
            tau_prev = prev.tau

        pred = self.plan[u][i].pred
        tau_pred = tau_prev
        if pred is not None:
            tau_pred = pred.tau

        curr.tau = max(tau_pred, tau_prev) + curr.getTime(self.simulation)
        if curr.a in self.arrival_times.keys():
            if curr.y == self.simulation.deliveries[curr.a].dst.ID:
                self.arrival_times[curr.a] = curr.tau
        next = None
        if i + 1 < len(self.plan[u]): next = self.plan[u][i + 1]
        succ = curr.succ
        if succ is not None:
            # need to find indices of succ
            for u_ in self.plan.keys():
                if succ in self.plan[u_]:
                    u_succ = u_
                    i_succ = self.plan[u_].index(succ)
                    print(f"\t should call succ u:{u_succ}, i:{i_succ}")
                    #self.updateTimes(u_succ, i_succ)
                    break
        #print(f"next {next}")
        if next != succ:
        #    print(f"\t calling next u:{u}, i:{i+1}")
            self.updateTimes(u, i+1)

        print("returning")'''

    def addBatterySwaps(self, plan_keys=[]):
        if plan_keys == []: plan_keys = self.plan.keys()

        for u in plan_keys:
            SOC = self.simulation.drones[u].SoC
            i = 0

            while i < len(self.plan[u]):
                w = 0
                if self.plan[u][i].a != -1:
                    if self.plan[u][i].a in self.simulation.deliveries.keys():
                        w = self.simulation.deliveries[self.plan[u][i].a].weight

                    consumption = self.simulation.cost(self.plan[u][i].x, self.plan[u][i].y, w)
                    #print(f"{SOC}: {self.plan[u][i].x} -- {self.plan[u][i].a} --> {self.plan[u][i].y}; {consumption}")

                    if SOC - consumption < 0:
                        # need a battery swap before action [u][i]
                        # impossile if [u][i-1] is a swap
                        # print(f"drone{u} action {i} has consumption {consumption} and current SoC is {SOC}")
                        self.plan[u] = self.plan[u][:i] + \
                                       [DroneAction(self.plan[u][i].x, self.plan[u][i].x, -1, 0)] + \
                                       self.plan[u][i:]
                        SOC = 1
                        i += 1
                    SOC -= consumption

                else:
                    # we need to check if the swap is necessary
                    # to do so we need to check if the next action is doable before the battery swap
                    if i == len(self.plan[u]) - 1:
                        self.plan[u] = self.plan[u][:i]
                    else: # if i  < len(self.plan[u]) - 1:
                        if self.plan[u][i + 1].a in self.simulation.deliveries.keys():
                            w = self.simulation.deliveries[self.plan[u][i + 1].a].weight
                        #assert self.plan[u][i+1].x in self.simulation.stations.keys()
                        #assert self.plan[u][i+1].y in self.simulation.stations.keys()
                        consumption = self.simulation.cost(self.plan[u][i + 1].x, self.plan[u][i + 1].y, w)

                        if SOC - consumption > 0:
                            # battery does not need to be swapped
                            self.plan[u] = self.plan[u][:i] + self.plan[u][i + 1:]
                            #i-=1 #
                        else:
                            SOC = 1
                            i += 1
                        SOC = SOC - consumption
                i += 1
            if len(self.plan[u]) > 0: self.updateTimes(u, 0)

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
                #if action.tau > CT: CT = action.tau
                if action.a in self.arrival_times.keys():
                    if action.y == self.simulation.deliveries[action.a].dst.ID:
                        self.arrival_times[action.a] = action.tau
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
                if action.a != -1:
                    MFT += action.getTime(self.simulation)
        return MFT/len(self.plan.keys())

    def getMeanSwapTime(self):
        MST = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.a == -1:
                    MST += action.getTime(self.simulation)
        return MST/len(self.plan.keys())

    def getMeanWaitingTime(self):
        return self.getMeanScheduleTime() - (self.getMeanFlightTime() + self.getMeanSwapTime())

    def getMeanDeliveryTime(self):
        MDT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                # if action.tau > CT: CT = action.tau
                if action.a in self.arrival_times.keys():
                    if action.y == self.simulation.deliveries[action.a].dst.ID:
                        self.arrival_times[action.a] = action.tau
                        MDT += self.arrival_times[action.a]
        return MDT/len(self.arrival_times.keys())

    def getMeanScheduleDistance(self):
        MSD = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.a >= 0:
                    MSD += self.simulation.dist2D(action.x, action.y)
        return MSD/len(self.plan.keys())

    def getMeanScheduleEnergy(self):
        MSE = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                w = 0
                if action.a in self.arrival_times.keys(): w = self.simulation.deliveries[action.a].weight
                if action.a >= 0:
                    MSE += self.simulation.cost(action.x, action.y, w)
        return MSE/len(self.plan.keys())

    def getMeanNumberSwaps(self):
        MNS = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.a == -1:
                    MNS += 1
        return MNS / len(self.plan.keys())

    def getDroneMeanUtilizationTime(self):
        '''
        This method computes the utilization time of drones in the system.
        Computed as the time drones spend flying or swapping batteries / ndrones
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
                    if action.a == d:
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

                if self.plan[u1][i].a not in self.simulation.stations.keys(): continue
                assert self.plan[u1][i].a != 0
                assert self.plan[u1][i].a != -1
                handover_station = self.plan[u1][i].x

                for u2 in self.plan.keys():
                    if u1 == u2: continue
                    if len(self.plan[u2]) == 0:
                        current_station = self.simulation.drones[u2].home.ID
                        if current_station == handover_station:
                            # handover
                            #print(f"handover for u{u1} at action {i} with u{u2} at its init station")
                            new_plan = copy.deepcopy(self.plan)
                            new_planu1 = copy.copy(new_plan[u1][:i])
                            new_planu2 = copy.copy(new_plan[u1][i:])
                            new_plan[u1] = new_planu1
                            new_plan[u2] = new_planu2
                            new_schedule = Schedule(self.simulation, new_plan)
                            new_schedule.addBatterySwaps([u1, u2])
                            if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2,0):
                                if new_schedule.getScheduleTime() < H:
                                    self.isValid()
                                    new_schedule.isValid()
                                    N.append(new_schedule)

                        else:
                            # add movement current_station -> handover_station, 0, 0
                            #print(f"handover for u{u1} at action {i} with u{u2} at adding a movement at its init station")
                            augmented_plan = self.addDroneMovement(u2, 0, handover_station)
                            if augmented_plan is not None:
                                new_plan = copy.deepcopy(augmented_plan)
                                new_planu1 = copy.copy(new_plan[u1][:i])
                                new_planu2 = copy.copy(new_plan[u2]) + copy.copy(new_plan[u1][i:])
                                new_plan[u1] = new_planu1
                                new_plan[u2] = new_planu2
                                new_schedule = Schedule(self.simulation, new_plan)
                                new_schedule.addBatterySwaps([u1, u2])
                                if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2, 0):
                                    if new_schedule.getScheduleTime() < H:
                                        self.isValid()
                                        new_schedule.isValid()
                                        N.append(new_schedule)
                    else:
                        for j in range(len(self.plan[u2])):
                            if self.plan[u2][j].a == -1: continue
                            #print(f"\t\t\t u{u2} at j={j}")
                            current_station = self.plan[u2][j].x

                            if current_station == handover_station:
                                #print(f"handover for u{u1} at action {i} with u{u2} at at action {j}")
                                # handover
                                new_plan = copy.deepcopy(self.plan)
                                assert new_plan[u1][i].x == new_plan[u2][j].x
                                new_planu1 = copy.copy(new_plan[u1][:i]) + copy.copy(new_plan[u2][j:])
                                new_planu2 = copy.copy(new_plan[u2][:j]) + copy.copy(new_plan[u1][i:])
                                new_plan[u1] = new_planu1
                                new_plan[u2] = new_planu2

                                new_schedule = Schedule(self.simulation, new_plan)
                                new_schedule.addBatterySwaps([u1, u2])
                                if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2,0):
                                    if new_schedule.getScheduleTime() < H:
                                        new_schedule.isValid()
                                        N.append(new_schedule)
                            else:
                                # add movement current_station -> handover_station, action, 0
                                #print(f"handover for u{u1} at action {i} with u{u2} at at augemnted action {j+1}")
                                augmented_plan = self.addDroneMovement(u2, j, handover_station)
                                if augmented_plan is not None:

                                    new_plan = copy.deepcopy(augmented_plan)
                                    assert new_plan[u1][i].x == new_plan[u2][j+1].x
                                    new_planu1 = copy.copy(new_plan[u1][:i]) + copy.copy(new_plan[u2][j+1:])
                                    new_planu2 = copy.copy(new_plan[u2][:j+1]) + copy.copy(new_plan[u1][i:])
                                    new_plan[u1] = new_planu1
                                    new_plan[u2] = new_planu2
                                    new_schedule = Schedule(self.simulation, new_plan)
                                    new_schedule.addBatterySwaps([u1, u2])
                                    if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2, 0):
                                        if new_schedule.getScheduleTime() < H:
                                            self.isValid()
                                            new_schedule.isValid()
                                            N.append(new_schedule)
        return N


    def addDroneMovement(self, u: int, i: int, s: int):
        assert u in self.plan.keys()
        assert i <= len(self.plan[u])
        new_plan = copy.deepcopy(self.plan)

        if len(self.plan[u]) == 0:
            # adding the first move
            curr_st = self.simulation.drones[u].home.ID
            if (curr_st, s) in self.simulation.edges and self.simulation.cost(curr_st, s, 0) <= 1:
                new_plan[u] = [DroneAction(curr_st, s, 0, 0)]

                return new_plan
        else:
            curr = new_plan[u][i]
            if curr.a != -1:
                set_predsucc = False
                w = 0
                if curr.a in self.simulation.deliveries.keys():
                    w = self.simulation.deliveries[curr.a].weight
                    set_predsucc = True

                if (curr.x, s) in self.simulation.edges and (s, curr.y) in self.simulation.edges and self.simulation.cost(curr.x, s, w) <= 1 and self.simulation.cost(s, curr.y, w) <= 1:
                    action1 = DroneAction(curr.x, s, curr.a, 0)
                    action2 = DroneAction(s, curr.y, curr.a, 0)
                    if set_predsucc:
                        if curr.succ is not None: curr.succ.pred = action2
                        if curr.pred is not None: curr.pred.succ = action1
                        action1.pred = curr.pred
                        action1.succ = action2
                        action2.pred = action1
                        action2.succ = curr.succ

                    new_plan[u] = new_plan[u][:i] + [action1, action2] + new_plan[u][i + 1:]
                    return new_plan

        return None



