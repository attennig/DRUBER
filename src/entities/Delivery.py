from src.entities.Station import *
class Delivery:
    def __init__(self, ID: int, ws_src: Station, ws_dst: Station, weight: float):
        self.ID = ID
        self.src = ws_src
        self.dst = ws_dst
        self.weight = weight



    def printInfo(self):
        print(f"Mission source: {self.src.ID}")
        print(f"Mission destination: {self.dst.ID}")
        print(f"Parcel weight: {self.weight}")

    def getAsDict(self):
        return {
            "src" : self.src.ID,
            "dst": self.dst.ID,
            "weight": self.weight
        }