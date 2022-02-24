import networkx as nx
class Greedy:
    def __init__(self, sim):
        print("\tinitializing Greedy Solver")
        self.simulation = sim
        G = nx.Graph()
        G.add_edges_from(self.simulation.edges)

    def computeShortestPath(self, d: int):
        assert d in self.simulation.deliveries.keys()
