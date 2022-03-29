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



    def updateTimes(self, u, i):
        # no handover greed needs to update only next --> to be updated for local search
        if i >= len(self.plan[u]): return
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
            for u_ in self.plan.keys():
                if succ in self.plan[u_]:
                    u_succ = u_
                    i_succ = self.plan[u_].index(succ)
                    self.updateTimes(u_succ, i_succ)
                    break

        if next is not None and next != succ:
            self.updateTimes(u, i+1)

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
                        print(f"drone{u} action {i} has consumption {consumption} and current SoC is {SOC}")
                        self.plan[u] = self.plan[u][:i] + \
                                       [DroneAction(self.plan[u][i].x, self.plan[u][i].x, -1, 0)] + \
                                       self.plan[u][i:]
                        SOC = 1
                        i += 1
                    else:
                        SOC -= consumption

                else:
                    # we need to check if the swap is necessary
                    # to do so we need to check if the next action is doable before the battery swap
                    if i + 1 < len(self.plan[u]):
                        if self.plan[u][i + 1].a in self.simulation.deliveries.keys():
                            w = self.simulation.deliveries[self.plan[u][i + 1].a].weight
                        consumption = self.simulation.cost(self.plan[u][i + 1].x, self.plan[u][i + 1].y, w)
                        if SOC - consumption > 0:
                            # battery does not need to be swapped
                            self.plan[u] = self.plan[u][:i] + self.plan[u][i + 1:]
                        else:
                            SOC = 1
                            i += 1
                i += 1
            self.updateTimes(u, 0)

    def getCompletionTime(self):
        CT = 0
        for u in self.plan.keys():
            for action in self.plan[u]:
                if action.a in self.arrival_times.keys():
                    if action.y == self.simulation.deliveries[action.a].dst.ID:
                        self.arrival_times[action.a] = action.tau
                        if action.tau > CT: CT = action.tau

        return CT

    def computeNeighbours(self):
        N = []

        for u1 in self.plan.keys():
            for u2 in self.plan.keys():
                if u1 == u2: continue
                for i in range(len(self.plan[u1])):
                    for j in range(len(self.plan[u2])):
                        if self.plan[u1][i].y == self.plan[u2][j].y:
                            new_plan = copy.copy(self.plan)
                            new_plan[u1] = copy.copy(self.plan[u1][:i+1]) + copy.copy(self.plan[u2][j+1:])
                            new_plan[u2] = copy.copy(self.plan[u2][:j+1]) + copy.copy(self.plan[u1][i+1:])
                            new_schedule = Schedule(self.simulation, new_plan)
                            new_schedule.addBatterySwaps([u1,u2])
                            new_schedule.updateTimes(u1, i)
                            new_schedule.updateTimes(u2, j)
                            if new_schedule.getCompletionTime() <= HORIZON:
                                N.append(new_schedule)

        for u in self.plan.keys():
            # add
            if len(self.plan[u]) == 0:
                for s in self.simulation.stations.keys():
                    if (self.simulation.drones[u].home.ID,s) in self.simulation.edges and self.simulation.cost(self.simulation.drones[u].home.ID,s,0) <= 1:
                        new_plan = copy.deepcopy(self.plan)
                        new_plan[u] = [DroneAction(self.simulation.drones[u].home, s, 0, 0)]
                        new_schedule = Schedule(self.simulation, new_plan)
                        new_schedule.addBatterySwaps([u])
                        new_schedule.updateTimes(u, 0)
                        if new_schedule.getCompletionTime() <= HORIZON:
                            N.append(new_schedule)


            for i in range(len(self.plan[u])):

                curr = self.plan[u][i]
                action = curr.a
                if curr.a == -1:
                    if i+1 <len(self.plan[u]):
                        next = self.plan[u][i + 1]
                        action = next.a
                    else: action = 0
                w = 0
                if curr.a in self.simulation.deliveries.keys():
                    w = self.simulation.deliveries[curr.a].weight

                for s in self.simulation.stations.keys():
                    if (curr.x,s) in self.simulation.edges and (s,curr.y) in self.simulation.edges and self.simulation.cost(curr.x,s,w) <= 1 and self.simulation.cost(s,curr.y,w) <= 1:

                        new_plan = copy.deepcopy(self.plan)
                        # add between i and i+1
                        new = [DroneAction(curr.x,s,action,0), DroneAction(s,curr.y,action,0)]
                        new_plan[u] = new_plan[u][:i] + new + new_plan[u][i+1:]
                        new_schedule = Schedule(self.simulation, new_plan)
                        new_schedule.addBatterySwaps([u])
                        new_schedule.updateTimes(u, 0)
                        if new_schedule.getCompletionTime() <= HORIZON:
                            N.append(new_schedule)

        print(len(N))
        return N