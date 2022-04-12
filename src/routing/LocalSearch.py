from src.routing.PathPlanner import *
from src.routing.Greedy import Greedy
class LocalSearch(PathPlanner):

    def __init__(self, sim, algo):
        print("\tinitializing Local Search Solver")
        PathPlanner.__init__(self, sim)
        self.algo = algo

    def setupProblem(self):
        pass

    def solveProblem(self):
        if self.algo == "HC":
            start_time = time.time()
            solution = self.hillClimbing()
            self.exec_time = time.time() - start_time
        elif self.algo == "LB":
            start_time = time.time()
            solution = self.localBeam()
            self.exec_time = time.time() - start_time
        elif self.algo == "BFSOPT":
            start_time = time.time()
            solution = self.BFSOPT()
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
            state = sorted(neighbours, key=lambda state: state.getCompletionTime())[0]


    def BFSOPT(self):
        objstate = self.stateInit()

        Q = [objstate]

        while len(Q) > 0:
            state = Q.pop()
            if state.getCompletionTime() < objstate.getCompletionTime():
                objstate = state
            neighbours = state.computeNeighbours(objstate.getCompletionTime())
            for n in neighbours:
                Q += [n]
        return objstate

    def hillClimbing(self):
        state = self.stateInit()
        objstate = state
        while True:
            if state.getCompletionTime() < objstate.getCompletionTime():
                objstate = state
            neighbours = state.computeNeighbours(state.getCompletionTime()) # empty if neighbours are not better than current state
            if len(neighbours) == 0: return objstate
            state = sorted(neighbours, key=lambda state: state.getCompletionTime())[0]

    def localBeam(self):
        objstate = self.stateInit()
        k = 5
        # best k neighbours of initial state for the first round
        neighbours = objstate.computeNeighbours(objstate.getCompletionTime())
        neighbours = sorted(neighbours, key=lambda state: state.getCompletionTime())[:k]

        while True:
            # for each round
            new_neighbours = []
            for state in neighbours:
                if state.getCompletionTime() < objstate.getCompletionTime():
                    objstate = state
                new_neighbours += state.computeNeighbours(state.getCompletionTime())
            # we recompute the best k neigbours of states selected in the previous round
            neighbours = sorted(new_neighbours, key=lambda state: state.getCompletionTime())[:k]

            if len(neighbours) == 0: return objstate

    def stateInit(self):
        greedySolver = Greedy(self.simulation)
        solution = greedySolver.solveProblem()
        return solution

    def getRunTime(self):
        pass