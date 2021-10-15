from Simulation import *
'''

'''

if __name__ == "__main__":
    DATAPATHS = [f'../data/{filename}.json' for filename in ['owners','waystations', 'drones', 'customers']]
    Sim = Simulation(DATAPATHS)
    Sim.loadData()
    #Sim.loadMissions("../data/missions.in")
    O = Sim.ownerRegistration()
    home = Sim.wayStationRegistration(O, 5.0, 5.0)
    Sim.droneRegistration(O, home)
    Sim.saveStatus()
    Sim.loadMissions("../data/missions.in")
    Sim.mapFig()