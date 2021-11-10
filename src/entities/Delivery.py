from src.entities.WayStation import *
class Delivery:
    def __init__(self, ID, ws_src, ws_dst, weight):
        #print(f"{type(ws_src)},{type(ws_dst)}:{WayStation}")
        assert type(ID) is int
        assert type(ws_src) is WayStation
        assert type(ws_dst) is WayStation
        assert type(weight) is float
        self.src = ws_src
        self.dst = ws_dst
        self.weight = weight

    def printInfo(self):
        print(f"Mission source: {self.src.ID}")
        print(f"Mission destination: {self.dst.ID}")
        print(f"Parcel weight: {self.weight}")

