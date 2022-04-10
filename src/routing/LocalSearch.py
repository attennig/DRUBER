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

    def exp(self):
        state = self.stateInit()
        for i in range(300):
            neighbours = state.computeNeighbours()
            print(f"visiting \n{state}\n\twith value {state.getCompletionTime()}")
            state = sorted(neighbours, key=lambda state: state.getCompletionTime())[-1]


    def BFSwithTTL(self):

        objstate = self.stateInit()

        Q = [objstate]

        while len(Q) > 0:
            state = Q.pop()
            for u in state.plan.keys(): 
                if len(state.plan[u]) > 0: assert state.plan[u][0].a != -1
            #print(f"visiting \n{state}\n\twith value {state.getCompletionTime()}")
            #print(f"To visit: {len(Q)}, currTTL: {currTTL}")
            if state.getCompletionTime() < objstate.getCompletionTime():
                objstate = state
            neighbours = state.computeNeighbours(objstate.getCompletionTime())
            for n in neighbours:
                Q += [n]
        return objstate

    def stochasticHillClimbing(self):
        pass
    def stateInit(self):
        greedySolver = Greedy(self.simulation)
        solution = greedySolver.solveProblem()
        return solution

    def getRunTime(self):
        pass