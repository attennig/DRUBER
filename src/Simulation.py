from Owner import *
from Customer import *
from Drone import *
from WayStation import *
from Mission import *
from Commitment import *
import json

class Simulation:
    def __init__(self, paths):
        self.owners = {}
        self.wayStations = {}
        self.drones = {}
        self.customers = {}
        self.count = 0
        self.VERBOSE = False
        self.DATAPATHS = paths

    def showStatus(self):
        if not self.VERBOSE: return
        print(f"The system has a total of {len(self.owners)} owners")
        for key in self.owners:
            self.owners[key].printInfo()
        print(f"The system has a total of {len(self.customers)} customers")
        for key in self.customers:
            self.customers[key].printInfo()

    def loadData(self):
        self.loadOwners(self.DATAPATHS[0])
        self.loadWayStations(self.DATAPATHS[1])
        self.loadDrones(self.DATAPATHS[2])
        self.loadCustomers(self.DATAPATHS[3])
        if self.VERBOSE: self.showStatus()

    def loadOwners(self, path):
        with open(path) as fin:
            data = json.load(fin)
            owners = data["Owners"]
            for owner in owners:
                self.owners[owner["ID"]] = Owner(owner["ID"])

    def loadWayStations(self, path):
        with open(path) as fin:
            data = json.load(fin)
            wayStations = data["WayStations"]
            for ws in wayStations:
                self.wayStations[ws['ID']] = WayStation(ws['ID'], ws['x'], ws['y'])
                self.owners[ws['Owner']].addWayStation(self.wayStations[ws['ID']])

    def loadDrones(self, path):
        with open(path) as fin:
            data = json.load(fin)
            drones = data["Drones"]
            for drone in drones:
                dID = drone['ID']
                oID = drone['Owner']
                homeWS = self.wayStations[drone['HomeWS']]
                self.drones[dID] = Drone(dID, homeWS)
                self.owners[oID].addDrone(self.drones[dID])

    def loadCustomers(self, path):
        with open(path) as fin:
            data = json.load(fin)
            customers = data["Customers"]
            for customer in customers:
                self.customers[customer["ID"]] = Customer(customer["ID"])

    def loadMissions(self, input_filename):
        commitments = []
        with open(input_filename, "r") as fin:
            n_missions = int(fin.readline())
            for i in range(n_missions):
                cID, msrcID, mdstID, budget, n_commitments = fin.readline().split(',')
                for i in range(int(n_commitments)):
                    dID, dsrcID, ddstID, cost = fin.readline().split(',')
                    dsrcWS = self.wayStations[int(dsrcID)]
                    ddstWS = self.wayStations[int(ddstID)]
                    commitments.append(Commitment(dsrcWS, ddstWS, float(cost)))
                msrcWS = self.wayStations[int(msrcID)]
                mdstWS = self.wayStations[int(mdstID)]
                M = Mission(msrcWS, mdstWS, float(budget))
                M.collectCommitments(commitments)
                M.findPath()

    def ownerRegistration(self):
        oID = max(self.owners) + 1
        assert oID not in self.owners.keys()
        self.owners[oID] = Owner(oID)
        return self.owners[oID]

    def wayStationRegistration(self, owner, x, y):
        assert type(owner) == Owner
        assert owner.ID in self.owners.keys()
        assert type(x) == float and type(x) == type(y)
        wsID = max(self.wayStations) + 1
        assert wsID not in self.wayStations.keys()
        self.wayStations[wsID] = WayStation(wsID, x, y)
        owner.addWayStation(self.wayStations[wsID])
        return self.wayStations[wsID]

    def droneRegistration(self, owner, homeWS):
        assert type(homeWS) == WayStation
        assert homeWS in owner.wayStations
        dID = max(self.drones) + 1
        assert dID not in self.drones.keys()
        self.drones[dID] = Drone(dID, homeWS)
        return self.drones[dID]

    def customerRegistration(self):
        cID = max(self.customers) + 1
        assert cID not in self.customers.keys()
        self.customers[cID] = Customer(cID)
        return self.customers[cID]

    def saveStatus(self):
        data = {"Owners": [{"ID":self.owners[oID].ID} for oID in self.owners.keys()]}
        with open(f"{self.DATAPATHS[0]}.out", 'w') as fout: json.dump(data,fout)
        data = {"WayStations": [{"ID": ws.ID, "Owner": oID, "x": ws.x, "y": ws.y} for oID in self.owners.keys() for ws in self.owners[oID].wayStations]}
        with open(f"{self.DATAPATHS[1]}.out", 'w') as fout: json.dump(data, fout)
        data = {"Drones": [{"ID": d.ID, "Owner": oID, "HomeWS": d.homeWS.ID} for oID in self.owners.keys() for d in self.owners[oID].drones]}
        with open(f"{self.DATAPATHS[2]}.out", 'w') as fout: json.dump(data, fout)
        data = {"Customers": [{"ID": self.customers[cID].ID} for cID in self.customers.keys()]}
        with open(f"{self.DATAPATHS[3]}.out", 'w') as fout: json.dump(data, fout)

    def mapFig(self):
        import matplotlib.pyplot as plt
        X = [self.wayStations[wsID].x for wsID in self.wayStations.keys()]
        Y = [self.wayStations[wsID].y for wsID in self.wayStations.keys()]
        plt.scatter(X,Y, marker='^')
        plt.show()

'''
    def findDrone(self, id):
        pass

    
    def customerRegistration(self, cID):
        assert type(cID) == int
        customer = Customer(cID, self)
        self.customers.add(customer)
        return customer

    def receiveRequest(self, src_id, dst_id, budget):
        src = self.findWayStation(src_id)
        dst = self.findWayStation(dst_id)
        mission = Mission(src, dst, budget)
        for owner in self.owners:
            owner.receiveMissionRequest(mission)
        def loadScenario(self, input_filename):
            with open(input_filename, "r") as fin:
                n_owners, n_customers = fin.readline().split(',')
                for i in range(int(n_owners)):
                    oID, n_WS, n_D = fin.readline().split(',')
                    owner = self.ownerRegistration(int(oID))
                    for j in range(int(n_WS)):
                        owner.addWayStation(WayStation(int(fin.readline())))
                    for j in range(int(n_D)):
                        dID, homeWSID = fin.readline().split(',')
                        homeWS = owner.getWayStation(int(homeWSID))

                        assert homeWS is not None
                        owner.addDrone(Drone(int(dID), homeWS))

                for i in range(int(n_customers)):
                    cID = fin.readline()
                    customer = self.customerRegistration(int(cID))
            self.showStatus()
        def loadMissions(self, input_filename):

            commitments = []
            with open(input_filename, "r") as fin:
                n_missions = int(fin.readline())
                for i in range(n_missions):
                    cID, msrcID, mdstID, budget, n_commitments = fin.readline().split(',')
                    print(f"creating mission src {msrcID}, dst {mdstID}, budget {budget}")
                    for i in range(int(n_commitments)):
                        dID, dsrcID, ddstID, cost = fin.readline().split(',')
                        dsrcWS = self.findWayStation(int(dsrcID))
                        ddstWS = self.findWayStation(int(ddstID))
                        commitments.append(Commitment(dsrcWS, ddstWS, float(cost)))

                    msrcWS = self.findWayStation(int(msrcID))
                    mdstWS = self.findWayStation(int(mdstID))
                    M = Mission(msrcWS, mdstWS, float(budget), self)
                    M.printInfo()
                    M.collectCommitments(commitments)
                    M.printInfo()
                    M.findPath()
    '''