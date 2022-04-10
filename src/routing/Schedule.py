from src.routing.DroneAction import *
import copy
class Schedule:
    def __init__(self, simulation, plan=None):
        self.simulation = simulation
        self.plan = plan
        if self.plan is None:
            self.plan = {u : [] for u in self.simulation.drones.keys()}

        #self.isValid()

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
            for i in range(len(self.plan[u])):
                #print(f"ACTOIN x{action.x}, y{action.y}")
                assert self.plan[u][i].a in [-1,0] or self.plan[u][i].a in self.simulation.deliveries.keys()
                assert self.plan[u][i].x in self.simulation.stations.keys()
                assert self.plan[u][i].y in self.simulation.stations.keys()
                if i > 0: assert self.plan[u][i].tau >= self.plan[u][i-1].tau

    def updateTimes(self, u, i):
        #print(f"to update from u={u}, i={i}")
        if i >= len(self.plan[u]): return True
        toUpdate = [(u,i)]
        updated = []
        #print(f"updating times: {u} {i} \n{self}")
        while len(toUpdate) > 0:

            curr_u, curr_i = toUpdate.pop(0)
            #print(f"u{curr_u}, i{curr_i}: {toUpdate}")
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
                tau_pred = pred.tau
            curr.tau = max(tau_pred, tau_prev) + curr.getTime(self.simulation)
            #print(f"predecessor:{tau_pred}, previous:{tau_prev}, curr:{curr.getTime(self.simulation)}->{curr.tau}")
            updated.append((curr_u, curr_i))

            next = None
            #print(self.plan[curr_u])
            if curr_i + 1 < len(self.plan[curr_u]):
                toUpdate.append((curr_u, curr_i+1)) # next to be updated
                next = self.plan[curr_u][curr_i+1]
            succ = curr.succ
            if succ is not None and succ != next:
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
                    if i == len(self.plan[u]):
                        self.plan[u] = self.plan[u][:i]
                    if i + 1 < len(self.plan[u]):
                        if self.plan[u][i + 1].a in self.simulation.deliveries.keys():
                            w = self.simulation.deliveries[self.plan[u][i + 1].a].weight
                        #assert self.plan[u][i+1].x in self.simulation.stations.keys()
                        #assert self.plan[u][i+1].y in self.simulation.stations.keys()
                        consumption = self.simulation.cost(self.plan[u][i + 1].x, self.plan[u][i + 1].y, w)

                        if SOC - consumption > 0:
                            # battery does not need to be swapped
                            self.plan[u] = self.plan[u][:i] + self.plan[u][i + 1:]
                        else:
                            SOC = 1
                            i += 1
                i += 1
            if len(self.plan[u]) > 0: self.updateTimes(u, 0)

    def getCompletionTime(self):
        CT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                #if action.tau > CT: CT = action.tau
                if action.a in self.arrival_times.keys():
                    if action.y == self.simulation.deliveries[action.a].dst.ID:
                        self.arrival_times[action.a] = action.tau
                        if action.tau > CT: CT = action.tau

        return CT
    def getScheduleTime(self):
        CT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.tau > CT: CT = action.tau
        return CT


    def computeNeighbours(self, H):
        N = []
        for u1 in self.plan.keys():
            #print(f"handover for {u1}")
            for i in range(len(self.plan[u1])):

                if self.plan[u1][i].a not in self.simulation.stations.keys(): continue
                assert self.plan[u1][i].a != 0
                assert self.plan[u1][i].a != -1
                #print(f"\tat {i} with parcel {self.plan[u1][i].a}")
                handover_station = self.plan[u1][i].x

                for u2 in self.plan.keys():
                    if u1 == u2: continue
                    #print(f"\t\ttry {u2}")
                    if len(self.plan[u2]) == 0:
                        #print(f"\t\t\t at {0}")
                        current_station = self.simulation.drones[u2].home.ID
                        if current_station == handover_station:
                            # handover
                            new_plan = copy.deepcopy(self.plan)
                            new_plan[u1] = copy.deepcopy(self.plan[u1][:i])
                            new_plan[u2] = copy.deepcopy(self.plan[u1][i:])
                            new_schedule = Schedule(self.simulation, new_plan)
                            new_schedule.addBatterySwaps([u1, u2])
                            if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2,0):
                                if new_schedule.getScheduleTime() < H:
                                    #print(f"{new_schedule.getCompletionTime()} <= {HORIZON}")
                                    self.isValid()
                                    new_schedule.isValid()

                                    #print(f"\t\t\t\tsuccessful handover resulting in \n{new_schedule}")
                                    N.append(new_schedule)

                        else:

                            # add movement current_station -> handover_station, 0, 0
                            augmented_plan = self.addDroneMovement(u2, 0, handover_station)

                            if augmented_plan is not None:
                                new_plan = copy.deepcopy(augmented_plan)
                                new_plan[u1] = copy.deepcopy(augmented_plan[u1][:i])
                                new_plan[u2] = copy.deepcopy(augmented_plan[u2]) + copy.deepcopy(augmented_plan[u1][i:])
                                new_schedule = Schedule(self.simulation, new_plan)
                                new_schedule.addBatterySwaps([u1, u2])
                                if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2, 0):
                                    if new_schedule.getScheduleTime() < H:
                                        #print(f"{new_schedule.getCompletionTime()} <= {HORIZON}")
                                        #print(f"handover at {u1} {i} action {self.plan[u1][i].a} with {u2} {len(augmented_plan[u2])-1}")
                                        self.isValid()
                                        new_schedule.isValid()
                                        #print(f"\t\t\t\tsuccessful handover resulting in \n{new_schedule}")
                                        N.append(new_schedule)

                    else:

                        for j in range(len(self.plan[u2])):

                            if self.plan[u2][j].a == -1: continue

                            current_station = self.plan[u2][j].x

                            if current_station == handover_station:
                                #print(f"\t\t\t at {j}")
                                # handover
                                new_plan = copy.deepcopy(self.plan)
                                assert new_plan[u1][i].x == new_plan[u2][j].x
                                new_plan[u1] = copy.deepcopy(self.plan[u1][:i]) + copy.deepcopy(self.plan[u2][j:])
                                new_plan[u2] = copy.deepcopy(self.plan[u2][:j]) + copy.deepcopy(self.plan[u1][i:])
                                new_schedule = Schedule(self.simulation, new_plan)
                                new_schedule.addBatterySwaps([u1, u2])
                                if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2,0):
                                    if new_schedule.getScheduleTime() < H:
                                        #rint(f"{new_schedule.getCompletionTime()} <= {HORIZON}")
                                        #print(f"self {self}")
                                        new_schedule.isValid()
                                        #print(f"\t\t\t\tsuccessful handover resulting in \n{new_schedule}")
                                        N.append(new_schedule)
                            else:
                                # add movement current_station -> handover_station, action, 0
                                augmented_plan = self.addDroneMovement(u2, j, handover_station)
                                if augmented_plan is not None:

                                    new_plan = copy.deepcopy(augmented_plan)
                                    #print(f"searching handover {u1} {i}, {u2} {j+1}")
                                    #self.printplan(new_plan)

                                    assert new_plan[u1][i].x == new_plan[u2][j+1].x
                                    new_plan[u1] = copy.deepcopy(augmented_plan[u1][:i]) + copy.deepcopy(augmented_plan[u2][j+1:])
                                    new_plan[u2] = copy.deepcopy(augmented_plan[u2][:j+1]) + copy.deepcopy(augmented_plan[u1][i:])
                                    new_schedule = Schedule(self.simulation, new_plan)
                                    new_schedule.addBatterySwaps([u1, u2])
                                    #print(new_schedule)
                                    #print(f"{u1} - {i}, {u2} - {j}")
                                    if new_schedule.updateTimes(u1, 0) and new_schedule.updateTimes(u2, 0):
                                        if new_schedule.getScheduleTime() < H:
                                            #print(f"{new_schedule.getCompletionTime()} <= {HORIZON}")
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

