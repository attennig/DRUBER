from Drone import *
from WayStation import *

class Owner:
    def __init__(self, ID):
        assert type(ID) == int
        self.ID = ID
        self.drones = set()
        self.wayStations = set()

    def addDrone(self, drone):
        assert type(drone) == Drone
        self.drones.add(drone)

    def addWayStation(self, wayStation):
        assert type(wayStation) == WayStation
        self.wayStations.add(wayStation)

    def getWayStation(self, id):
        for ws in self.wayStations:
            if ws.ID == id:
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