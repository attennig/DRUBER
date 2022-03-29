from src.routing.PathPlanner import *
from src.routing.Greedy import Greedy
class LocalSearch(PathPlanner):

    def __init__(self, sim):
        print("\tinitializing Local Search Solver")
        PathPlanner.__init__(self, sim)

    def setupProblem(self):
        pass

    def solveProblem(self):
        start_time = time.time()
        solution = self.BFSwithTTL()
        self.exec_time = time.time() - start_time
        return solution

    def BFS(self):
        print("BFS")
        objstate = self.stateInit()

        Q = [objstate]
        V = []
        while len(Q) > 0:
            state = Q.pop()
            #print(f"State: {state}")
            if state.getCompletionTime() < objstate.getCompletionTime():
                objstate = state
            V.append(state)
            neighbours = state.computeNeighbours()
            Q += [n for n in neighbours if n not in V]
        return objstate

    def BFSwithTTL(self):
        print("BFS with TTL")
        objstate = self.stateInit()
        TTL_init = 2
        Q = [(objstate, TTL_init)]

        while len(Q) > 0:
            state, currTTL = Q.pop()
            for u in state.plan.keys(): assert state.plan[u][0].a != -1
            print(f"visiting \n{state}\n\twith value {state.getCompletionTime()}")
            print(f"To visit: {len(Q)}, currTTL: {currTTL}")
            if state.getCompletionTime() < objstate.getCompletionTime():
                objstate = state
            if currTTL > 0:
                neighbours = state.computeNeighbours()
                for n in neighbours:
                    if n.getCompletionTime() < objstate.getCompletionTime():
                        newTTL = currTTL + 1
                    elif n.getCompletionTime() < state.getCompletionTime():
                        newTTL = currTTL
                    else:
                        newTTL = currTTL - 1
                    Q += [(n, newTTL)]
        return objstate


    def stateInit(self):
        greedySolver = Greedy(self.simulation)
        solution = greedySolver.solveProblem()
        return solution

    def getRunTime(self):
        pass