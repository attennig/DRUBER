from Drone import *
from WayStation import *
from Mission import *
class Owner:
    def __init__(self, ID, sim):
        self.SIMULATION = sim
        assert type(ID) == int
        self.ID = ID
        self.drones = []
        self.wayStations = []

    def addDrone(self, drone):
        assert type(drone) == Drone
        self.drones.append(drone)

    def addWayStation(self, wayStation):
        assert type(wayStation) == WayStation
        self.wayStations.append(wayStation)

    def getWayStation(self, id):
        for ws in self.wayStations:
            if ws.ID == id:
                if self.SIMULATION.VERBOSE: print(f"found of type {type(ws)}")
                return ws
        return None

    '''def receiveMissionRequest(self, mission):
        pass'''
    def printInfo(self):
        print(f"owner {self.ID} has {len(self.drones)} drones and {len(self.wayStations)} way stations registered")
        print(f"drones:")
        for d in self.drones: d.printInfo()
        print(f"way stations:")
        for ws in self.wayStations: ws.printInfo()

