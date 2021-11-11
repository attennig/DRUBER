from src.entities.WayStation import *
class Delivery:
    def __init__(self, ID: int, ws_src: WayStation, ws_dst: WayStation, weight: float):
        self.src = ws_src
        self.dst = ws_dst
        self.weight = weight
        self.currentStation = ws_src

    def updateStation(self, ws: WayStation):
        self.currentStation = ws

    def printInfo(self):
        print(f"Mission source: {self.src.ID}")
        print(f"Mission destination: {self.dst.ID}")
        print(f"Parcel weight: {self.weight}")

