from PathPlanner  import *
from WayStation import *
class Mission:
    def __init__(self, ws_src, ws_dst, budget):
        assert type(ws_src) == WayStation
        assert type(ws_dst) == WayStation
        assert type(budget) == float
        self.src = ws_src
        self.dst = ws_dst
        self.budget = budget
        self.commitments = []
        self.pathPlanner = PathPlanner()

    def printInfo(self):
        print(f"Mission source: {self.src.ID}")
        print(f"Mission destination: {self.dst.ID}")
        print(f"Currently {len(self.commitments)} commitments have been collected")
        for c in self.commitments:
            c.printInfo()

    def collectCommitments(self, commitments):
        self.commitments = commitments

    def findPath(self):
        self.pathPlanner.findPath(self, self.commitments)