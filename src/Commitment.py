from WayStation import *
class Commitment:
    def __init__(self, src, dst, cost):
        assert type(src) == WayStation
        assert type(dst) == WayStation
        assert type(cost) == float
        self.src = src
        self.dst = dst
        self.cost = cost

    def printInfo(self):
        print(f"from {self.src.ID} to {self.dst.ID} with cost {self.cost}")