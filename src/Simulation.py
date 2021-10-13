from Owner import *
from Customer import *
from Drone import *
from WayStation import *
from Mission import *
import json
class Simulation:
    def __init__(self, paths):
        self.owners = {}
        self.wayStations = {}
        self.drones = {}
        self.customers = {}
        self.count = 0
        self.VERBOSE = True
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
        self.showStatus()

    def loadOwners(self, path):
        with open(path) as fin:
            data = json.load(fin)
            owners = data["Owners"]
            for owner in owners:
                self.owners[owner["ID"]] = Owner(owner["ID"], self)

    def loadWayStations(self, path):
        with open(path) as fin:
            data = json.load(fin)
            wayStations = data["WayStations"]
            for ws in wayStations:
                self.wayStations[ws['ID']] = WayStation(ws['ID'])
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
                self.customers[customer["ID"]] = Customer(customer["ID"], self)

    def findWaystation(self, id):
        for owner in self.owners:
            ws = owner.getWayStation(id)
            if ws is not None: return ws
        return None

    def loadMissions(self, input_filename):
        commitments = []
        with open(input_filename, "r") as fin:
            n_missions = int(fin.readline())
            for i in range(n_missions):
                cID, msrcID, mdstID, budget, n_commitments = fin.readline().split(',')
                print(f"creating mission src {msrcID}, dst {mdstID}, budget {budget}")
                for i in range(int(n_commitments)):
                    dID, dsrcID, ddstID, cost = fin.readline().split(',')
                    dsrcWS = self.wayStations[int(dsrcID)]
                    ddstWS = self.wayStations[int(ddstID)]
                    commitments.append(Commitment(dsrcWS, ddstWS, float(cost)))

                msrcWS = self.wayStations[int(msrcID)]
                mdstWS = self.wayStations[int(mdstID)]
                M = Mission(msrcWS, mdstWS, float(budget), self)
                M.printInfo()
                M.collectCommitments(commitments)
                M.printInfo()
                M.findPath()
                print("ok")

'''
    def findDrone(self, id):
        pass


    def ownerRegistration(self, oID):
        assert type(oID) == int
        owner = Owner(oID,self)
        self.owners.add(owner)
        return owner

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