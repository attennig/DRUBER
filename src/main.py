from Simulation import *
'''

'''

if __name__ == "__main__":
    DATAPATHS = [f'../data/{filename}.json' for filename in ['owners','waystations', 'drones', 'customers']]
    Sim = Simulation(DATAPATHS)
    Sim.loadData()
    Sim.loadMissions("../data/missions.in")
