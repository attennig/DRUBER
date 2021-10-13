from WayStation import *
from Commitment import *
class Drone:
    def __init__(self, ID, homeWS):
        #self.SIMULATION = sim
        assert type(ID) == int
        assert type(homeWS) == WayStation
        self.ID = ID
        self.homeWS = homeWS

    def sendCommitment(self, request):
        pass

    def printInfo(self):
        print(f"drone ID: {self.ID}")
