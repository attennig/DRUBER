from math import sqrt, cos, sin, radians
import random
import json
import os
from src.simulation.Simulator import Simulator
from src.entities.Station import *
from src.entities.Drone import *
from src.entities.Delivery import *
from src.config import *
class RandomGenerator:
    def __init__(self, S: Simulator):
        self.simulation = S
        random.seed(self.simulation.seed)

    def generateRandomInstance(self, N_stations, N_Drones, N_Deliveries):
        print("Stations ")
        self.generateRandomStations(N_stations)
        print("Stations done")
        print("Drones ")
        self.generateRandomDrones(N_Drones)
        print("Drones done")
        print("Deliveries ")
        self.generateRandomDeliveries(N_Deliveries)
        print("Deliveries done")

    def generateRandomStations(self, N_stations):
        x, y = random.uniform(0, AoI_SIZE), random.uniform(0, AoI_SIZE)
        self.simulation.stations[1] = Station(1, x, y)
        j = 2
        while len(self.simulation.stations) < N_stations:
            i = random.randint(1, len(self.simulation.stations))
            max_dist = 1 / self.simulation.unitcost(DRONE_MAX_PAYLOAD)
            d, theta = random.uniform(MIN_DISTANCE,max_dist), radians(random.uniform(0, 360))
            x = self.simulation.stations[i].x + d * cos(theta)
            y = self.simulation.stations[i].y + d * sin(theta)
            if self.availableLocation(x, y):
                print(f"positioning {j} as neighbour of {i}")
                self.simulation.stations[j] = Station(j, x, y)
                j += 1

        self.simulation.computeEdges()

    def generateRandomDrones(self, N_Drones):
        S = [s for s in self.simulation.stations.keys()]
        for u in range(1, N_Drones + 1):
            home_u = random.choice(S)
            self.simulation.drones[u] = Drone(u, self.simulation.stations[home_u])

    def generateRandomDeliveries(self, N_Deliveries):
        for d in range(1, N_Deliveries + 1):
            S = [s for s in self.simulation.stations.keys()]
            rnd_src, rnd_dst = random.sample(S, 2)

            w = random.uniform(0, DRONE_MAX_PAYLOAD)
            self.simulation.deliveries[d] = Delivery(d, self.simulation.stations[rnd_src],
                                                     self.simulation.stations[rnd_dst], w)
    '''
    def generateRandomDrones(self, N_Drones):
        u = 1
        U = [] # used
        C = {} # capacities
        for s in self.simulation.stations.keys():
            C[s] = 0
        while u <= N_Drones:
            print(u)
            if len(U) < len(self.simulation.stations):
                S = [s for s in self.simulation.stations.keys() if s not in U]
            else:
                S = [s for s in self.simulation.stations.keys()]
            if u == 1:
                first = True
            else:
                first = False
            while len(S) > 0:
                R = {}
                L = {}
                for s in S:
                    R[s] = self.stationsReachableFrom(s, S, TIME_LIMIT * DRONE_SPEED)
                    L[s] = len(R[s])
                #print(R)
                home_u = max(L.keys(), key=L.get)
                #print(R)
                if C[home_u] <= self.simulation.stations[home_u].capacity:
                    self.simulation.drones[u] = Drone(u, self.simulation.stations[home_u])
                    #self.simulation.drones[u].printInfo()
                    S.remove(home_u)
                    U.append(home_u)
                    C[home_u] += 1
                    #print(f"{C[home_u]} < {self.simulation.stations[home_u].capacity}")

                for s in R[home_u]: S.remove(s)
                u += 1
                if u > N_Drones:
                    if first and len(S) > 0:
                        raise Exception("Error, N_Drones too small")
                    break
                full = True
                for s in self.simulation.stations.keys():
                    if C[s] <= self.simulation.stations[s].capacity: full = False
                if full and u <= N_Drones:
                    raise Exception("Error, N_Stations too small")
                    break
    

    
    def stationsReachableFrom(self, i, S, limit):
        #print(f"Computing reachable stations from {i}. Stations:{S}; limit:{limit}")
        Q = []
        dist = {}
        prev = {}
        R = set()
        for s in S:
            Q.append(s)
            dist[s] = float('inf')
            prev[s] = None
        dist[i] = 0
        while len(Q) > 0:
            u = min(dist.keys() & Q, key=dist.get)
            Q.remove(u)
            N = [v for (s, v) in self.simulation.edges if s == u and v in Q]
            for v in N:
                alt = dist[u] + self.simulation.dist2D(u, v)
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    if dist[v] <= limit:
                        R.add(v)
        return R
    '''
    def availableLocation(self, x, y):
        if not (0 < x < AoI_SIZE and 0 < y < AoI_SIZE): return False
        for s in self.simulation.stations.keys():
            if sqrt((self.simulation.stations[s].x - x) ** 2 + (
                    self.simulation.stations[s].y - y) ** 2) <= MIN_DISTANCE:
                #print(f"location ({x}, {y}) not available")
                return False
        return True


    def saveInstance(self):
        map = self.simulation.getMap() # seve as map.png
        map.savefig(f"{self.simulation.outFOLDER}/map_in.png") # img overlap

        stations = {}
        drones = {}
        deliveries = {}
        for s in self.simulation.stations.keys():
            stations[s] = self.simulation.stations[s].getAsDict()
        for u in self.simulation.drones.keys():
            drones[u] = self.simulation.drones[u].getAsDict()
        for d in self.simulation.deliveries.keys():
            deliveries[d] = self.simulation.deliveries[d].getAsDict()
        data = {'entities':
                    {
                        'stations': stations,
                        'drones': drones,
                        'deliveries': deliveries
                    }

                }  # save as in.json
        '''parameters':
        {
            'num_activities': self.simulation.num_activities,
            'path_len': self.simulation.path_len
        }'''

        with open(f"{self.simulation.outFOLDER}/in.json", "w") as file_out:
            json.dump(data, file_out)

        '''config = {
                    'SIMULATION_SEED': SIMULATION_SEED,
                    'AoI_SIZE': AoI_SIZE,
                    'HORIZON': HORIZON,
                    'SWAP_TIME': SWAP_TIME,
                    'DRONE_SPEED': DRONE_SPEED,
                    'DRONE_MAX_PAYLOAD': DRONE_MAX_PAYLOAD,
                    'MIN_DISTANCE': MIN_DISTANCE,
                    'UNIT_CONSUMPTION': UNIT_CONSUMPTION,
                    'ALPHA': ALPHA,
                    'CONSUMPTION_UPPER_BOUND': CONSUMPTION_UPPER_BOUND
                  } # save as config.json
        with open(f"{self.simulation.dataFOLDER}/config.json", "w") as file_out:
            json.dump(config, file_out)'''
